# Sword purchasing data. 
docker-compose exec mids ab -n 100 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword/red/2

docker-compose exec mids ab -n 100 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_sword/red/3

docker-compose exec mids ab -n 500 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_sword/red/1

docker-compose exec mids ab -n 200 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword/blue/1

docker-compose exec mids ab -n 200 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_sword/blue/2

docker-compose exec mids ab -n 10 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_sword/blue/3

docker-compose exec mids ab -n 300 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_sword/green/1

docker-compose exec mids ab -n 100 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_sword/green/1

docker-compose exec mids ab -n 100 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_sword/green/1


# Horse Purchasing Data
docker-compose exec mids ab -n 100 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_horse/1/small/1

docker-compose exec mids ab -n 500 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_horse/1/small/1

docker-compose exec mids ab -n 200 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_horse/1/small/1

docker-compose exec mids ab -n 200 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_horse/1/medium/2

docker-compose exec mids ab -n 400 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_horse/1/medium/1

docker-compose exec mids ab -n 300 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_horse/1/medium/1

docker-compose exec mids ab -n 50 -m POST -H "Host: user1.comcast.com" http://localhost:5000/purchase_a_horse/1/large/1

docker-compose exec mids ab -n 50 -m POST -H "Host: user2.comcast.com" http://localhost:5000/purchase_a_horse/1/large/1

docker-compose exec mids ab -n 500 -m POST -H "Host: user3.comcast.com" http://localhost:5000/purchase_a_horse/1/large/1


# Guild Activity Data
docker-compose exec mids ab -n 200 -m POST -H "Host: user1.comcast.com" http://localhost:5000/guild/join

docker-compose exec mids ab -n 100 -m POST -H "Host: user1.comcast.com" http://localhost:5000/guild/leave
