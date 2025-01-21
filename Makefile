PWD=$(shell pwd)
IMAGE?=python
APP_NAME=$(shell pwd | xargs basename)-${IMAGE}
APP_DIR = /${APP_NAME}
COMMAND?=bash
ENV_FILE=.env

YELLOW=$(shell printf '\033[0;1;33m')
COLOR_OFF=$(shell printf '\033[0;1;0m')

debug:
	@docker run -it \
		--env-file ${ENV_FILE} \
		-v ${PWD}:${APP_DIR} \
		-w ${APP_DIR} \
		--rm --name ${APP_NAME} ${IMAGE} \
		sh -c "${COMMAND}"

analyze-doc:
	@echo "${YELLOW}Analysing docs 🤖${COLOR_OFF}"
	@make -s debug COMMAND="pip install -r requirements.txt && bash"
