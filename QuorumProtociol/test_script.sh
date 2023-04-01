rm -rf files
mkdir files

echo "Starting Registry Server with Nr=2, Nw=2 and N=4"
python3 registryServer.py <<'EOF' &
2
3
4
EOF
sleep 3

echo "Starting 4 servers"


python3 server.py r1 8889 &
python3 server.py r2 8890 &
python3 server.py r3 8891 &
python3 server.py r4 8892 &


sleep 10
echo "Starting client"

python3 client.py test