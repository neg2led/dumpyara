#
# Copyright (C) 2022 Dumpyara Project
#
# SPDX-License-Identifier: GPL-3.0
#

from distutils.dir_util import copy_tree
from pathlib import Path
from sebaubuntu_libs.libaik import AIKManager
from sebaubuntu_libs.liblogging import LOGW

def extract_bootimg(file: Path, output_path: Path):
	aik_manager = AIKManager()
	try:
		image_info = aik_manager.unpackimg(file)
	except Exception:
		LOGW(f"Failed to extract {file.name}, invalid boot image")
		return None

	output_path.mkdir(parents=True)

	(output_path / "info.txt").write_text(str(image_info))

	if image_info.kernel:
		(output_path / "kernel").write_bytes(image_info.kernel.read_bytes())

	if image_info.dt:
		(output_path / "dt.img").write_bytes(image_info.dt.read_bytes())

	if image_info.dtb:
		(output_path / "dtb.img").write_bytes(image_info.dtb.read_bytes())

	if image_info.dtbo:
		(output_path / "dtbo.img").write_bytes(image_info.dtbo.read_bytes())

	if image_info.ramdisk:
		copy_tree(str(image_info.ramdisk), str(output_path / "ramdisk"), preserve_symlinks=True)

	aik_manager.cleanup()

	return output_path
