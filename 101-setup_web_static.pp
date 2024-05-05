# Define a class to set up the web servers for deployment of web_static
class web_server_setup {

    # Update package lists
    package { 'update_packages':
        ensure => latest,
        provider => 'apt',
    }

    # Upgrade installed packages
    package { 'upgrade_packages':
        ensure => latest,
        provider => 'apt',
    }

    # Install nginx
    package { 'nginx':
        ensure => installed,
        require => Package['update_packages', 'upgrade_packages'],
    }

    # Create necessary directories
    file { ['/data/web_static/releases/test', '/data/web_static/shared']:
        ensure => directory,
        owner  => 'ubuntu',
        group  => 'ubuntu',
        mode   => '0755',
    }

    # Create a test index.html file
    file { '/data/web_static/releases/test/index.html':
        ensure  => present,
        content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n',
        owner   => 'root',
        group   => 'root',
        mode    => '0644',
    }

    # Create a symbolic link to set current directory
    file { '/data/web_static/current':
        ensure => link,
        target => '/data/web_static/releases/test',
        owner  => 'root',
        group  => 'root',
    }

    # Configure Nginx
    file_line { 'add_hbnb_static_location':
        ensure  => present,
        path    => '/etc/nginx/sites-available/default',
        line    => "        location /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n",
        require => Package['nginx'],
    }

    # Start Nginx service
    service { 'nginx':
        ensure => running,
        enable => true,
        require => Package['nginx', 'add_hbnb_static_location'],
    }
}

# Apply the class to set up the web servers
include web_server_setup
