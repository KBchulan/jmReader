import sys
import json
import shutil
import time
import re
import os
from pathlib import Path
from datetime import datetime

print(f"Python路径: {sys.path}")
print(f"脚本路径: {__file__}")
print(f"当前工作目录: {os.getcwd()}")

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")
STATIC_PATH = "/static"
script_dir = os.path.dirname(os.path.abspath(__file__))  # app目录
backend_dir = os.path.dirname(script_dir)  # backend目录
TARGET_DIR = os.path.join(backend_dir, 'mock')

def get_static_url(path):
    if path.startswith('/'):
        path = path[1:]
    return f"{BASE_URL}{STATIC_PATH}/{path}"

print(f"下载脚本中的BASE_URL: {BASE_URL}")
print(f"下载脚本中的TARGET_DIR: {TARGET_DIR}")
print(f"当前工作目录: {Path.cwd().absolute()}")

def download_and_process(comic_id):
    """下载漫画并处理"""
    try:
        print(f"开始下载漫画 {comic_id}...")
        print(f"当前工作目录: {Path.cwd().absolute()}")

        before_dirs = set(d.name for d in Path(".").iterdir() if d.is_dir())
        print(f"下载前的目录: {before_dirs}")

        print(f"正在导入jmcomic模块...")
        try:
            import jmcomic
            print(f"jmcomic模块导入成功, 版本: {getattr(jmcomic, '__version__', '未知')}")
        except ImportError as e:
            print(f"导入jmcomic模块失败: {e}")
            print("请确保已安装jmcomic模块: pip install jmcomic")
            return False

        print(f"开始下载漫画ID: {comic_id}...")
        jmcomic.download_album(comic_id)

        time.sleep(2)

        after_dirs = set(d.name for d in Path(".").iterdir() if d.is_dir())
        new_dirs = after_dirs - before_dirs
        print(f"下载后新增的目录: {new_dirs}")

        if not new_dirs:
            print("下载完成，但找不到新增的目录")
            return False

        newest_dir = max(new_dirs, key=lambda d: Path(d).stat().st_mtime)
        source_path = Path(newest_dir)
        print(f"找到下载目录: {source_path.absolute()}")

        script_dir = Path(__file__).parent
        print(f"脚本目录: {script_dir.absolute()}")

        target_dir = Path(TARGET_DIR)
        print(f"最终目标目录: {target_dir.absolute()}")
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / comic_id
        print(f"漫画目标目录: {target_path.absolute()}")

        if target_path.exists():
            print(f"目标目录 {target_path} 已存在，正在删除...")
            shutil.rmtree(target_path)

        target_path.mkdir(parents=True, exist_ok=True)

        print(f"正在处理文件从 {source_path} 到 {target_path}...")

        image_files = []
        for ext in ['.jpg', '.png', '.webp']:
            image_files.extend(list(source_path.glob(f"*{ext}")))

        print(f"找到 {len(image_files)} 个图片文件")

        def extract_page_number(path):
            numbers = re.findall(r'\d+', path.stem)
            return int(numbers[0]) if numbers else 0

        image_files.sort(key=extract_page_number)

        image_paths = []
        for i, img_file in enumerate(image_files):
            new_name = f"{i+1:05d}{img_file.suffix}"
            dest_file = target_path / new_name
            print(f"复制 {img_file} -> {dest_file}")
            shutil.copy2(img_file, dest_file)
            image_paths.append(f"{comic_id}/{new_name}")

        title = source_path.name
        print(f"漫画标题: {title}")

        comic_info = {
            "id": comic_id,
            "title": title,
            "cover": image_paths[0] if image_paths else "",
            "author": "未知",
            "description": "从JM漫画下载的漫画",
            "tags": ["漫画", "JM漫画"],
            "updateTime": datetime.now().isoformat().split('T')[0],
            "status": "completed"
        }

        if source_path.exists():
            print(f"清理源目录: {source_path}")
            shutil.rmtree(source_path)

        update_comics_list(comic_id, comic_info, image_paths)

        print(f"漫画 {comic_id} 处理完成, 已添加到mock数据")
        return True
    except Exception as e:
        print(f"下载或处理漫画 {comic_id} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_comics_list(comic_id, comic_info, image_paths):
    """更新漫画列表"""
    try:
        print(f"开始更新漫画列表，漫画ID: {comic_id}")

        target_dir = Path(TARGET_DIR)
        print(f"最终目标目录: {target_dir.absolute()}")
        target_dir.mkdir(parents=True, exist_ok=True)

        comics_list_path = target_dir / "comics.json"
        print(f"漫画列表文件路径: {comics_list_path.absolute()}")

        if not comics_list_path.exists():
            print(f"漫画列表文件不存在，将创建新文件")
            comics_list = []
        else:
            print(f"读取现有漫画列表文件")
            with open(comics_list_path, "r", encoding="utf-8") as f:
                comics_list = json.load(f)
            print(f"读取到 {len(comics_list)} 个漫画")

        comic_exists = False
        for i, comic in enumerate(comics_list):
            if comic["id"] == comic_id:
                print(f"漫画 {comic_id} 已存在，更新信息")
                comics_list[i] = comic_info
                comic_exists = True
                break

        if not comic_exists:
            print(f"漫画 {comic_id} 不存在，添加到列表")
            comics_list.append(comic_info)

        print(f"保存更新后的漫画列表，共 {len(comics_list)} 个漫画")
        with open(comics_list_path, "w", encoding="utf-8") as f:
            json.dump(comics_list, f, ensure_ascii=False, indent=2)

        chapter = {
            "id": f"{comic_id}-1",
            "comicId": comic_id,
            "title": "第1话",
            "order": 1,
            "updateTime": datetime.now().isoformat().split('T')[0],
            "pageCount": len(image_paths)
        }

        chapters_path = target_dir / "chapters.json"
        print(f"章节列表文件路径: {chapters_path.absolute()}")

        if not chapters_path.exists():
            print(f"章节列表文件不存在，将创建新文件")
            chapters = []
        else:
            print(f"读取现有章节列表文件")
            with open(chapters_path, "r", encoding="utf-8") as f:
                chapters = json.load(f)
            print(f"读取到 {len(chapters)} 个章节")

        chapter_exists = False
        for i, ch in enumerate(chapters):
            if ch["id"] == chapter["id"]:
                print(f"章节 {chapter['id']} 已存在，更新信息")
                chapters[i] = chapter
                chapter_exists = True
                break

        if not chapter_exists:
            print(f"章节 {chapter['id']} 不存在，添加到列表")
            chapters.append(chapter)

        print(f"保存更新后的章节列表，共 {len(chapters)} 个章节")
        with open(chapters_path, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        print(f"漫画 {comic_id} 已成功添加到漫画列表")
    except Exception as e:
        print(f"更新漫画列表时出错: {e}")
        import traceback
        traceback.print_exc()

def main():
    comic_id = sys.argv[1] if len(sys.argv) > 1 else "416330"

    download_and_process(comic_id)

if __name__ == "__main__":
    main()
