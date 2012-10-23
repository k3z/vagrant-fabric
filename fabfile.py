from fabric.api import *
import fabtools.require

from fabtools.vagrant import vagrant # NOQA


@task
def upgrade():
    
    # update packages list and upgrade system before running install
    sudo("apt-get update")
    sudo("apt-get upgrade")
    

@task
def install():
        
    # install required packages (+extras) for LAMP server
    fabtools.require.deb.packages([
        # 'build-essential',
        # 'devscripts',
        'locales',
        'mc',
        # 'imagemagick',
        # 'ghostscript',
        'apache2',
        'sqlite3',
        'perl',
        'ruby',
        'php5',
        'php5-sqlite',
        'php5-mcrypt',
        'php5-mysql',        
    ], update=False)
    
    # add french locale set
    # fabtools.require.system.locale('fr_FR.UTF-8')
    
    # add mysql server and set default password for root
    fabtools.require.mysql.server(password='mypassword')
    
    # change Apache envvars and set vagrant has main user
    fabtools.require.files.template_file(
        template_source = './fabric/files/apache/envvars.template',
        path='/etc/apache2/envvars', 
        context = {
            'apache_run_user': 'vagrant',
            'apache_run_group': 'vagrant',
        },
        owner = 'root',
        group = 'root',
        use_sudo=True
    )

    # create a new virtual host and use ~/vagrant_www as document root
    fabtools.require.files.template_file(
        template_source = './fabric/files/apache/vhost.conf.template',
        path='/etc/apache2/sites-available/vagrant', 
        context = {
            'server_name': 'localhost',
            'port': 80,
            'document_root': '/vagrant_www',
        },
        owner = 'root',
        group = 'root',
        use_sudo=True
    )

    # enable new vhost
    if not fabtools.files.is_link('/etc/apache2/sites-enabled/vagrant'):
        sudo("a2dissite default")
        sudo("a2ensite vagrant")

    # activate mod_rewrite (usefull these days)
    if not fabtools.files.is_link('/etc/apache2/mods-enabled/rewrite.load'):
        sudo("a2enmod rewrite")
    
    # place php file for testing purpose
    fabtools.require.files.file(
        '/vagrant_www/info.php', 
        source='./fabric/files/php/info.php',
        owner = 'vagrant',
        group = 'vagrant',
        use_sudo=True
    )
    
    sudo("/etc/init.d/apache2 restart")
    