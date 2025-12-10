FROM php:7.4-apache

# Install PHP extensions
RUN docker-php-ext-install mysqli

# Enable Apache rewrite
RUN a2enmod rewrite

# Install sudo (needed for privesc)
RUN apt update && apt install -y sudo

# 🚨 Privilege Escalation Misconfiguration
# Allow www-data to run PHP as root with NO password
RUN echo "www-data ALL=(root) NOPASSWD: /usr/bin/php" > /etc/sudoers.d/www-data \
    && chmod 440 /etc/sudoers.d/www-data

# 🚩 Create root flag EVERY build
RUN echo 'uacCTF{Y0u_D1d_1T_Congratsss}' > /root/flag.txt \
    && chmod 600 /root/flag.txt

# Copy application
COPY src/app /var/www/html/
COPY src/static /var/www/html/static/

# Uploads writable
RUN chown -R www-data:www-data /var/www/html/uploads
