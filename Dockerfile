FROM php:7.4-apache

# Enable Apache rewrite & install PHP extensions
RUN a2enmod rewrite \
    && docker-php-ext-install mysqli

# Tools needed for privesc
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and build vulnerable SUID binary
COPY vuln.c /tmp/checksys.c
RUN gcc /tmp/checksys.c -o /usr/local/bin/checksys \
    && chown root:root /usr/local/bin/checksys \
    && chmod 4755 /usr/local/bin/checksys \
    && rm /tmp/checksys.c

# 🚩 Root flag
RUN echo 'uacCTF{SUID_PATH_HIJACK_PWNED}' > /root/flag.txt \
    && chmod 600 /root/flag.txt

# Copy web app files (excluding static to handle separately)
COPY src/app/*.php src/app/util.php src/app/api.php src/app/config.php /var/www/html/
COPY src/app/api/ /var/www/html/api/
COPY src/app/static/ /var/www/html/static/

# Writable uploads directory
RUN mkdir -p /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html/uploads