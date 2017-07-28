events {}

http {
    server {
        listen 80;

        {% for service in services %}
            location {{ service.public_path }} {
                proxy_pass {{ service.service.url }};
            }
        {% endfor %}

    }
}
