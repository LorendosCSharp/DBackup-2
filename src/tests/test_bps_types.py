import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("BACKUP_FILES_PATH", str(Path(tempfile.mkdtemp(prefix="dbackup-tests-"))))

from src.typed.backupDestinations.baseDestination import BaseBD, BaseBDPub
from src.typed.backupDestinations.sshDestination import SshBD, SshBDPub
from src.typed.backupDestinations.telegramDestination import TelegramBD, TelegramBDPub
from src.typed.backupService import BPS, BPSPub
from src.typed.backupTargets.baseTarget import BaseBT, BaseBTPub
from src.typed.backupTargets.container.containerBT import ContainerBT, ContainerBTPub
from src.typed.backupTargets.container.containerFileTarget import ContainerFileBT, ContainerFileBTPub
from src.typed.backupTargets.container.containerPostgresqlTarget import ContainerPostgresqlBT, ContainerPostgresqlBTPub
from src.typed.backupTargets.fileTarget import FileBT, FileBTPub
from src.typed.backupTargets.postgresqlTarget import PostgresqlBT, PostgresqlBTPub
from src.typed.docker.container import Container
from src.typed.docker.mount import Mount


class TestBpsTypedModels(unittest.TestCase):
    def _sample_container(self) -> Container:
        return Container(
            Names=["demo-db"],
            State="running",
            Id="container-abc",
            Mounts=[
                Mount(
                    Type="bind",
                    Name="demo-volume",
                    Source="/tmp/source",
                    Destination="/data",
                    Driver="local",
                    Mode="ro",
                    RW=False,
                    Propagation="rprivate",
                )
            ],
        )

    def test_bps_pub_converts_all_destination_and_target_variants(self):
        pub = BPSPub(
            name="typed-demo",
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
                BaseBTPub(type="base"),
                FileBTPub(type="file", path="/tmp/source.txt"),
                PostgresqlBTPub(type="postgres", path="/tmp/postgres.sql"),
                ContainerBTPub(type="container", container=self._sample_container()),
                ContainerFileBTPub(
                    type="c_file",
                    path="/tmp/container.txt",
                    container=self._sample_container(),
                ),
                ContainerPostgresqlBTPub(
                    type="c_postgres",
                    path="/tmp/container.sql",
                    container=self._sample_container(),
                ),
            ],
            cronTime="*_*_*_1_*_*_",
            include=True,
        )

        converted = BPS.from_pub(pub)

        self.assertEqual(converted.name, "typed-demo")
        self.assertEqual(len(converted.destinations), 3)
        self.assertIsInstance(converted.destinations[0], BaseBD)
        self.assertIsInstance(converted.destinations[1], SshBD)
        self.assertIsInstance(converted.destinations[2], TelegramBD)

        self.assertEqual(len(converted.targets), 6)
        self.assertIsInstance(converted.targets[0], BaseBT)
        self.assertIsInstance(converted.targets[1], FileBT)
        self.assertIsInstance(converted.targets[2], PostgresqlBT)
        self.assertIsInstance(converted.targets[3], ContainerBT)
        self.assertIsInstance(converted.targets[4], ContainerFileBT)
        self.assertIsInstance(converted.targets[5], ContainerPostgresqlBT)

        self.assertTrue(converted.id)


if __name__ == "__main__":
    unittest.main()
