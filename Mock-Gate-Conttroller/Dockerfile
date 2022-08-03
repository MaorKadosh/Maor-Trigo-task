FROM python:3.10-slim-buster
WORKDIR /mock_gate_controller
COPY . .

CMD [ "python", "-u", "mock_gate_controller.py", "--ip gate-mock", "--port 5000"]