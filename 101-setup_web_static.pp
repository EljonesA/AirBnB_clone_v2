# Ensure NGinx is installed and running
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure => running,
  enable => true,
  require => Package['nginx'],
}

# Create necessary directories
file { '/data/web_static/releases/test/':
  ensure => directory,
}

file { '/data/web_static/shared/':
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "Holberton School\n",
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  force  => true,
}

# Set ownership of /data/ folder to ubuntu:ubuntu
file { '/data/':
  ensure  => directory,
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Update NGinx configuration file to serve content of /data/web_static/current/ to hbnb_static
$location_block = "location /hbnb_static/ {\n\talias /data/web_static/current/;\n\tautoindex off;\n}\n"

file_line { 'add_location_block':
  path  => '/etc/nginx/sites-available/default',
  line  => $location_block,
  match => "^\\s*server\\s*{",
  notify => Service['nginx'],
}

# Restart NGinx to apply configuration changes
exec { 'restart_nginx':
  command => '/usr/sbin/service nginx restart',
  refreshonly => true,
}

# Ensure the script/program always exits successfully
exec { 'exit_successfully':
  command => '/bin/true',
}
