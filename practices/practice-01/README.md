В терминале ubuntu:
cd mobile-robots-project-seminar
HOST_XAUTHORITY="$XAUTHORITY" docker compose --env-file .env --env-file .env.local -f docker-compose.yaml -f docker-compose.gpu.yaml up -d
HOST_XAUTHORITY="$XAUTHORITY" docker compose --env-file .env --env-file .env.local -f docker-compose.yaml -f docker-compose.gpu.yaml exec -it ros2-base zsh

Потом в терминале контейнера:
cd ~/practices_ws
rm -rf build install log
colcon build --symlink-install
source install/setup.zsh
ros2 launch cherepaxa06 cherepaxa06.launch.py
