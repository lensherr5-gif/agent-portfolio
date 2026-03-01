from src.app.cli import main

if __name__ == "__main__":
    # 保持 CLI 程序的标准退出码行为。
    raise SystemExit(main())
