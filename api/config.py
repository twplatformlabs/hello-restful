"""
hello-restful api

api base configuration
"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field

DESCRIPTION = """
<a href="https://github.com/twplatformlabs/hello-restful"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/twplatformlabs/hello-restful"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/twplatformlabs/hello-restful"></a>
<div align="center">
	<p>
		<img alt="twplatformlabs" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/banner.png?sanitize=true" width=400 />
	</p>
  <h1>Lightweight RESTful API simulator and testing endpoint</h1>
</div>
<br />
"""

# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """base settings"""
    title: str = "hello-restful"
    description: str = DESCRIPTION
    prefix: str = "/hello"
    debug: bool = False
    releaseId: str = Field(default_factory=lambda: os.environ.get("API_VERSION", "snapshot"))
    version: str = "v1"
    server_info_url: str = "http://localhost:15000/server_info"

settings = Settings()
route_prefix = f"/{settings.version}{settings.prefix}"
