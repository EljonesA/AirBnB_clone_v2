# File: setup_web_static.pp

# Install NGINX package
package { 'nginx':
  ensure => installed,
}

# Ensure NGINX service is running
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Create necessary directories if they don't exist
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared']:
  ensure => directory,
}

# Create a sample HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "Hi Eljones👋, I am served from Nginx.\n",
}

# Create symbolic link between /data/web_static/current and /data/web_static/releases/test/
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  force   => true,
  require => File['/data/web_static/releases/test/index.html'],
}

# Give ownership of /data/ folder to user/group "ubuntu"
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Update NGINX configuration to serve content of /data/web_static/current/ to hbnb_static
file_line { 'nginx_hbnb_static':
  path    => '/etc/nginx/sites-available/default',
  line    => "location /hbnb_static/ {\n\talias /data/web_static/current/;\n\tautoindex off;\n}\n",
  match   => "^\\s*server\\s*{",
  notify  => Service['nginx'],
  require => File['/data/web_static/current'],
}