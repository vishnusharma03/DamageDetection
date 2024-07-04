# Damage Detection

- This project demonstrates the end-to-end process of training and deploying a machine learning model for detecting car damages using YOLOv8.
- The model is build & deployed for end users in a scalable environment.
- The model is trained on a custom dataset of car damages, including scratches, dents, and other common issues. 
-The containerized model is pushed to Amazon Elastic Container Registry (ECR) and deployed using Amazon Elastic Container Service (ECS).
- This project demonstrates how to import a custom ML model to AWS & deploy it.

## Structure
```
.
├── CustomAlgorithm.ipynb
├── Dockerfile
├── ReadMe.md
├── build_and_push.sh
├── container
│   ├── extract.py
│   ├── nginx.conf
│   ├── predictor.py
│   ├── script
│   ├── serve
│   ├── train
│   └── wsgi.py
├── index.html
├── opt
│   └── ml
│       ├── input
│       │   ├── config
│       │   │   └── hyperparameters.json
│       │   └── data
│       │       └── training
│       │           └── data.yaml
│       ├── model
│       │   ├── train
│       │   │   └── weights
│       │   │       ├── best.pt
│       │   │       └── last.pt
│       │   └── yolov8n.pt
│       └── output
│           └── failure
├── requirements.txt
└── task_05-revision1.json
```

## Prerequisites
- Docker
- AWS CLI (configured)

## Installation
```
# Clone the repo
git clone https://github.com/vishnusharma03/DamageDetection.git
cd DamageDetection

# Build the docker image
docker build -t damage:latest .

# Push the image to ECR
chmod +x build_and_push.sh
./build_and_push.sh damage

# Use ECR & ECS to deploy it
```

## Insights Gained

- Linux based Commands
- Docker containerization
- Using AWS to deploy a server using nginx & gunicorn
- Using AWS ECR & ECS
- Understanding of domain & ssl

## License

This project is licensed under the MIT License.