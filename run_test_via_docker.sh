TEST_PATH="${1}"

docker run \
--rm \
--privileged \
-w=/app \
--memory=4g \
--cpus=2 \
-v "$(pwd)/allure_results:/app/allure_results" \
--name="blaxemeter_selenium_gheckoFireFox" \
${DOCKER_IMAGE_NAME} \
"${TEST_PATH}" -v -W ignore:DeprecationWarning