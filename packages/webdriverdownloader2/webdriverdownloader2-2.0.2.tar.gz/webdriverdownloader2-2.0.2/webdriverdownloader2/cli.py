import argparse
import os
import os.path

from webdriverdownloader2 import (
    ChromeDriverDownloader,
    GeckoDriverDownloader,
)


downloaders = {
    "chrome": ChromeDriverDownloader,
    "firefox": GeckoDriverDownloader,
}


def parse_command_line():
    parser = argparse.ArgumentParser(
        description=u"Tool for downloading and installing WebDriver binaries."
    )
    parser.add_argument(
        u"browser",
        help=(
            u"Browser to download the corresponding WebDriver binary.  Valid values are: {0}.  "
            u'Optionally specify a version number of the WebDriver binary as follows: "browser:version" '
            u'e.g. "chrome:2.39".  If no version number is specified, the latest available version of the '
            u"WebDriver binary will be downloaded."
        ).format(", ".join(['"' + browser + '"' for browser in downloaders.keys()])),
        nargs="+",
    )
    return parser.parse_args()


def main():
    args = parse_command_line()
    for browser in args.browser:
        if ":" in browser:
            browser, version = browser.split(":")
        else:
            version = "latest"
        if browser.lower() in downloaders.keys():
            print(f"Downloading WebDriver for browser: '{browser}'")
            downloader = downloaders[browser]()
            extracted_binary, link = downloader.download_and_install(version)
            print(f"Driver binary downloaded to: {extracted_binary}")
            if os.path.islink(link):
                print(f"Symlink created: {link}")
            else:
                print(f"Driver copied to: {link}")
        else:
            print(f"Unrecognized browser: '{browser}'.  Ignoring...")
        print("")

    link_path = os.path.split(link)[0]
    if link_path not in os.environ["PATH"].split(os.pathsep):
        print(
            f"WARNING: Path '{link_path}' is not in the PATH environment variable."
        )


if __name__ == "__main__":
    main()
