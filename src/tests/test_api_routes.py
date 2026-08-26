import os
import tempfile
import unittest
from pathlib import Path
from typing import Literal
from unittest.mock import patch

os.environ.setdefault("BACKUP_FILES_PATH", str(Path(tempfile.mkdtemp(prefix="dbackup-tests-"))))

from fastapi.testclient import TestClient
from src.api.routers.docker import docker as docker_router
from src.core import bpsManager
from src.main import app
from src.typed.backupDestinations.baseDestination import BaseBD, BaseBDPub
from src.typed.backupDestinations.sshDestination import SshBDPub
from src.typed.backupDestinations.telegramDestination import TelegramBDPub
from src.typed.backupService import BPS, BPSPub
from src.typed.backupTargets.baseTarget import BaseBT
from src.typed.backupTargets.container.containerBT import ContainerBTPub
from src.typed.backupTargets.container.containerFileTarget import ContainerFileBTPub
from src.typed.backupTargets.container.containerPostgresqlTarget import ContainerPostgresqlBTPub
from src.typed.backupTargets.fileTarget import FileBTPub
from src.typed.backupTargets.postgresqlTarget import PostgresqlBTPub
from src.typed.docker.container import Container
from src.typed.docker.mount import Mount


class RecordingTarget(BaseBT):
    type: Literal["base"] = "base"
    file_name: str = "artifact.tar.gz"

    def package(self, BPSId: str) -> str:
        backup_dir = Path(bpsManager.outputPath) / BPSId
        backup_dir.mkdir(parents=True, exist_ok=True)
        archive_path = backup_dir / self.file_name
        archive_path.write_text("test-backup-content")
        return str(archive_path)


class RecordingDestination(BaseBD):
    type: Literal["base"] = "base"
    sent_paths: list[str] = []

    def sendTo(self, path: str):
        self.sent_paths.append(path)


class TestApiRoutes(unittest.TestCase):
    def setUp(self):
        bpsManager.BPSList.clear()
        self.client = TestClient(app)

    def _sample_bps_payload(self) -> dict:
        sample_container = {
            "Names": ["example-db"],
            "State": "running",
            "Id": "container-123",
            "Mounts": [
                {
                    "Type": "bind",
                    "Name": "db",
                    "Source": "/tmp/db",
                    "Destination": "/data",
                    "Driver": "local",
                    "Mode": "ro",
                    "RW": False,
                    "Propagation": "rprivate",
                }
            ],
        }

        payload = BPSPub(
            name="demo-bps",
            destinations=[
                BaseBDPub(type="base"),
                SshBDPub(
                    type="ssh",
                    user="backup-user",
                    ip="127.0.0.1",
                    port=22,
                    keyPath="/tmp/id_rsa",
                    remoteDirectory="/tmp/remote",
                ),
                TelegramBDPub(
                    type="tg",
                    chatId=1234,
                    botKeyPath="/tmp/bot.env",
                ),
            ],
            targets=[
                FileBTPub(type="file", path="/tmp/source.txt"),
                ContainerBTPub(type="container", container=Container(**sample_container)),
                ContainerFileBTPub(
                    type="c_file",
                    path="/tmp/container.txt",
                    container=Container(**sample_container),
                ),
                ContainerPostgresqlBTPub(
                    type="c_postgres",
                    path="/tmp/container.sql",
                    container=Container(**sample_container),
                ),
            ],
            cronTime="*_*_*_1_*_*_",
            include=True,
        )
        return payload.model_dump(mode="json")

    def test_docs_routes_are_available(self):
        switcher = self.client.get("/docs2/")
        legacy = self.client.get("/docs2/legacy")
        current = self.client.get("/docs2/current")

        self.assertEqual(switcher.status_code, 200)
        self.assertEqual(legacy.status_code, 200)
        self.assertEqual(current.status_code, 200)

        self.assertIn("DBackup-Server", legacy.text)
        self.assertIn("Current project-state documentation", current.text)

    def test_bps_crud_and_backup_ops(self):
        payload = self._sample_bps_payload()

        create_response = self.client.post("/bps/", json=payload)
        self.assertEqual(create_response.status_code, 200, create_response.text)
        created = create_response.json()
        bps_id = created["id"]

        list_response = self.client.get("/bps/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 1)

        one_response = self.client.get(f"/bps/{bps_id}")
        self.assertEqual(one_response.status_code, 200)
        self.assertEqual(one_response.json()["id"], bps_id)

        updated_payload = dict(payload)
        updated_payload["name"] = "updated-demo-bps"
        update_response = self.client.put(f"/bps/{bps_id}", json=updated_payload)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["name"], "updated-demo-bps")

        delete_response = self.client.delete(f"/bps/{bps_id}")
        self.assertEqual(delete_response.status_code, 200)

    def test_trigger_backup_writes_artifact_and_sends_it_to_destination(self):
        with tempfile.TemporaryDirectory(prefix="dbackup-backup-") as temp_root:
            destination = RecordingDestination(id="dest-1")
            destination.sent_paths.clear()
            target = RecordingTarget(id="target-1")
            bps = BPS(
                name="backup-flow-check",
                destinations=[destination],
                targets=[target],
                cronTime="*_*_*_1_*_*_",
                include=True,
                id="backup-flow-check",
            )

            bpsManager.BPSList = [bps]
            with patch.object(bpsManager, "outputPath", temp_root):
                result = bpsManager.triggerBackup(bps.id)

            self.assertEqual(len(result["generated"]), 1)
            archive_path = Path(result["generated"][0])
            self.assertTrue(archive_path.exists())
            self.assertEqual(result["sent"], [str(archive_path)])
            self.assertEqual(destination.sent_paths, [str(archive_path)])

    def test_docker_routes_return_container_payloads(self):
        fake_container = {
            "Id": "abc123",
            "Name": "demo-container",
            "State": {"Status": "running"},
            "Mounts": [
                {
                    "Type": "bind",
                    "Name": "demo-volume",
                    "Source": "/tmp/source",
                    "Destination": "/data",
                    "Mode": "ro",
                    "RW": False,
                    "Propagation": "rprivate",
                }
            ],
        }

        fake_containers = [type("FakeContainer", (), {"attrs": fake_container})()]

        with patch.object(docker_router, "listAllContainers", return_value=fake_containers), \
             patch.object(docker_router, "extractRunningContainers", return_value=fake_containers):
            containers = self.client.get("/docker/containers")
            running = self.client.get("/docker/containers/running")

        self.assertEqual(containers.status_code, 200)
        self.assertEqual(running.status_code, 200)
        self.assertEqual(len(containers.json()), 1)
        self.assertEqual(len(running.json()), 1)


if __name__ == "__main__":
    unittest.main()
