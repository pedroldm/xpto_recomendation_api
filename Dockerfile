FROM python:3.12.1-slim

RUN apt-get update && apt-get install -y build-essential git python3-dev libpq-dev

RUN pip install poetry

RUN git clone https://github.com/pedroldm/xpto_recommendation_api.git

WORKDIR /xpto_recommendation_api

RUN poetry install

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]