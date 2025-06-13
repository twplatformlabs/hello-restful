<div align="center">
  <p>
    <img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/twplatformlabs/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
    <img alt="DPS Title" src="https://raw.githubusercontent.com/twplatformlabs/static/master/dps_lab_title.png" width=350/>
  </p>
  <h3>Lightweight API providing request and response endpoints</h3>
  <h1>hello-restful</h1>
  <a href="https://app.circleci.com/pipelines/github/twplatformlabs/hello-restful"><img src="https://circleci.com/gh/twplatformlabs/hello-restful.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/twplatformlabs/circleci-remote-docker"></a>
</div>
<br />

hello-restful is a small, fastapi service designed to be deployed on kubernetes and provide common http request/response endpoints and demonstrate using an openapi framework for automated api documentation.  

Access at [https://twplatformlabs.org/v1/hello](https://twplatformlabs.org/v1/hello).  
OAS documentation [here](https://twplatformlabs.org/v1/hello/apidocs).  _pending_

To run locally on docker:  
```bash
docker run -it -d -p 8000:8000 ghcr.io/twplatformlabs/hello-restful  
```
Access on http://localhost:8000/v1/hello  

## local developement  

**run locally with uvicorn**  

```
uvicorn api.main:api --reload
```
