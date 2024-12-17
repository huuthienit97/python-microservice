# Python Microservices với FastAPI và ArangoDB

Dự án backend sử dụng kiến trúc microservices với FastAPI, ArangoDB và API Gateway.

## Cấu trúc dự án

```
.
├── api_gateway/          # API Gateway service
├── services/            
│   ├── user_service/    # Quản lý người dùng
│   ├── auth_service/    # Xác thực và phân quyền
│   └── product_service/ # Quản lý sản phẩm
├── docker-compose.yml   # Cấu hình Docker
└── requirements.txt     # Dependencies
```

## Yêu cầu hệ thống

- Python 3.12+
- Docker và Docker Compose
- pip3

## Cài đặt

1. Tạo môi trường ảo:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
.\venv\Scripts\activate  # Windows
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Khởi động các services:
```bash
docker-compose up --build
```

## Các endpoints

- API Gateway: http://localhost:8000
- User Service: http://localhost:8001
- Auth Service: http://localhost:8002
- Product Service: http://localhost:8003
- ArangoDB UI: http://localhost:8529

## Phát triển

Mỗi service được thiết kế để hoạt động độc lập và giao tiếp thông qua API Gateway. Sử dụng ArangoDB làm cơ sở dữ liệu chung.
# python-microservice
