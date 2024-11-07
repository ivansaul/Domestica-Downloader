# CHANGELOG

## v0.1.0 (2024-11-07)

### Chore

* chore: setup CI/CD with semantic release

Setup CI/CD workflows for testing and automatic releases using semantic release. This ensures consistent versioning, automated testing, and simplified release management. ([`2f561e5`](https://github.com/ivansaul/Domestica-Downloader/commit/2f561e536e1820ec4a234c4342c19e9717936cf5))

* chore: setup mypy to ignore missing imports ([`b57c926`](https://github.com/ivansaul/Domestica-Downloader/commit/b57c9263ae0438dbd5bcfaa7436a8ef96f972ec0))

### Feature

* feat: add course URL to course model

Adds a URL field to the Course model to store the course&#39;s URL. This makes it easier to access and track the source of each course. ([`427876f`](https://github.com/ivansaul/Domestica-Downloader/commit/427876f278e0afa69b3a365d52d15bea0df20918))

* feat: extract course ID from URL

Adds a function to extract the course ID from a Domestika URL. ([`d819d87`](https://github.com/ivansaul/Domestica-Downloader/commit/d819d87ab8008d63e56330cee74c0dd33ddfc3ba))

* feat: improve string sanitation

Add a helper function to clean strings, removing special characters and whitespace for better consistency in titles and metadata. ([`19d29c2`](https://github.com/ivansaul/Domestica-Downloader/commit/19d29c24b624038fbb708d6fa956c8dd2776558a))

* feat: add dependency management func

The implementation downloads a specific version of dep, extracts the necessary files, and sets up the binary&#39;s executable permissions and to the system&#39;s PATH environment variable for easy access. ([`f3e0b9e`](https://github.com/ivansaul/Domestica-Downloader/commit/f3e0b9e11e55e33dae31333df5f91fe91cc17bd5))

* feat: parallelize section fetching

Fetch all sections concurrently using asyncio to improve performance. This significantly reduces the time required to retrieve course data by leveraging asynchronous operations. ([`1347dc5`](https://github.com/ivansaul/Domestica-Downloader/commit/1347dc525532aa13fee0aacd0252ba1592695a48))

* feat: add initial cli and download functionality

Includes initial download functionality for videos and assets ([`78e2100`](https://github.com/ivansaul/Domestica-Downloader/commit/78e2100b2c4ae5dc3a0c4751eef4040f608dc681))

### Fix

* fix: prevent fetching of unsupported course types

Adds a check to prevent fetching of multi-course pages, which are currently unsupported. ([`2886b9c`](https://github.com/ivansaul/Domestica-Downloader/commit/2886b9c961332dcd92c38beeb4739e32ae0cc2ba))

* fix: close browser tab when somo error occur ([`fb29004`](https://github.com/ivansaul/Domestica-Downloader/commit/fb29004a9976b8a6b2222aa93a7d4a7e6d87af7f))

* fix: close browser tabs after use ([`5576f6e`](https://github.com/ivansaul/Domestica-Downloader/commit/5576f6ed4d6c3779cdf994ee4c0eb0533dd7efe9))

* fix: close browser page after fetching course data

Close the browser page after fetching course data to prevent resource leaks and ensure proper cleanup. ([`2aa0d25`](https://github.com/ivansaul/Domestica-Downloader/commit/2aa0d253644feb66da8ef85e10054dd7bbd986c9))

### Refactor

* refactor: CourseInfo model ([`87b8885`](https://github.com/ivansaul/Domestica-Downloader/commit/87b888528cd182a49b9b00da8bcaf679db796b2e))

### Unknown

* Merge pull request #1 from ivansaul/feature/semantic-release

Feature/semantic release ([`91a5045`](https://github.com/ivansaul/Domestica-Downloader/commit/91a5045997ff75565bb5fb384d4d13150da6a98d))
