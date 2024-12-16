from .server import serve

def main():
    """Main entry point for the package."""
    import asyncio
    asyncio.run(serve())

__all__ = ["main", "server"]

if __name__ == "__main__":
    main()
