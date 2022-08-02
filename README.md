# ISH Processo Seletivo

Instructions to run the code:
* git clone https://github.com/raryelcostasouza/ishProcessoSelectivo.git

* Run locally
* cd ishProcessoSelectivo
* pipenv --three
* pipenv --install
* ./bootstrap.sh

To Run with Docker
* sudo docker build -t safelabs .
* sudo docker run --name safelabs -d -p 5000:5000 safelabs

* Request formats accepted:
curl -X POST -H "Content-Type: application/json" -d '{
    "city": "brasilia"
}' http://localhost:5000/weatherplaylist

curl -X POST -H "Content-Type: application/json" -d '{
    "lat": "-15.7797",     
    "long": "-47.9297"
}' http://localhost:5000/weatherplaylist
