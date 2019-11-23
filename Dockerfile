FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install nbformat pyyaml

COPY . .

ENTRYPOINT python run-playbook.py && jupyter nbconvert --execute --to html result.ipynb --TemplateExporter.exclude_input=True && mv result.html output/