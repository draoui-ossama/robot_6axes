install(
  DIRECTORY config/
  DESTINATION share/${PROJECT_NAME}/config
)

install(
  DIRECTORY urdf/ launch/
  DESTINATION share/${PROJECT_NAME}
)