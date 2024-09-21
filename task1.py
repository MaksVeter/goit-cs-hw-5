# -*- coding: utf-8 -*-

import argparse
import os
import asyncio
import aiofiles
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s', filename='errors.log')



async def copy_file(file_path, target_dir):
    try:
        ext = file_path.suffix[1:].lower()
        if not ext:
            ext = 'unknown'

        target_folder = target_dir / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        destination = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy, file_path, destination)
    except Exception as e:
        logging.error(f"Помилка копіювання файлу {file_path}: {e}")



async def read_folder(source_dir, target_dir):
    try:
        for root, dirs, files in os.walk(source_dir):
            tasks = []
            for file in files:
                file_path = Path(root) / file
                tasks.append(copy_file(file_path, target_dir))
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка читання папки {source_dir}: {e}")



def main():
    parser = argparse.ArgumentParser(
        description="Асинхронне сортування файлів по підпапках на основі їх розширення.")
    parser.add_argument("source_folder", type=str,
                        help="Вихідна папка з файлами")
    parser.add_argument("output_folder", type=str,
                        help="Цільова папка для сортування файлів")

    args = parser.parse_args()

    source_dir = Path(args.source_folder)
    target_dir = Path(args.output_folder)

    if not source_dir.is_dir():
        print(f"Вихідна папка {source_dir} не існує.")
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    asyncio.run(read_folder(source_dir, target_dir))


if __name__ == "__main__":
    main()
