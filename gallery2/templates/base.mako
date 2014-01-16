<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>${SITE_NAME}</title>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">

    <!-- Optional theme -->
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">
    <!-- <link rel="stylesheet" href="//bootswatch.com/cerulean/bootstrap.min.css"> -->
    <link rel="stylesheet" href="//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css">
    
    % for url in assets('css'):
    <link href="${url}" rel="stylesheet">
    % endfor 
    <!-- Add custom CSS here -->
    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->

  </head>

  <body>
    <noscript>Please enable JavaScript in your browser.</noscript>

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="${route_url('home')}">${SITE_NAME}</a>
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse navbar-ex1-collapse">
          <ul class="nav navbar-nav">
                <li${' class="active"' if self.attr.active_tab == 'tags' else '' | n}><a href="${route_url('tags')}">Tags</a></li>
                % if has_permission('upload'):
              <li${' class="active"' if self.attr.active_tab == 'upload' else '' | n}><a href="${route_url('upload')}">Upload</a></li>
                % endif
          </ul>
          <ul class="nav navbar-nav pull-right">
            % if request.user:
            <li><a href="${route_url('profile', request.user, slug=request.user.username)}">${request.user.username}</a></li>
            <li><a href="${route_url('logout')}">Logout</a></li>
            % else:
            <li><a href="${login_url}">Login</a></li>
            <li><a href="${route_url('signup')}">Signup</a></li>
            % endif
          </ul>
          <form class="navbar-form navbar-left" role="search" action="${route_url('search')}" method="GET">
              <div class="form-group">
                <input type="text" class="form-control tags" name="q" placeholder="Search">
              </div>
              <button type="submit" class="btn btn-default"><i class="glyphicon glyphicon-search"></i></button>
            </form>

        </div><!-- /.navbar-collapse -->
      </div><!-- /.container -->
    </nav>
    <!-- messages -->
    <div class="container">
        % for queue in ['success', 'info', 'warning', 'danger']:
            % for message in request.session.pop_flash(queue):
            <div class="alert alert-{{queue}} alert-dismissable">
                 <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                ${message}
            </div>
            % endfor
        % endfor
    </div>
    <!-- end messages -->


    <div class="container">
        ${next.body()}
    </div><!-- /.container -->
    
    <div class="container">

      <hr>

      <footer>
        <div class="row">
          <div class="col-lg-12">
            <p>Copyright &copy; Company 2013</p>
          </div>
        </div>
      </footer>

    </div><!-- /.container -->

    <!-- JavaScript -->
    <script src="//code.jquery.com/jquery.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/ui/1.10.3/jquery-ui.js"></script>

    % for url in assets('js'):
    <script type="text/javascript" src="${url}"></script>
    % endfor

  </body>
</html>

