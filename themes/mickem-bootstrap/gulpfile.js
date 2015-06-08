var gulp       = require('gulp');
    gutil      = require('gulp-util');
var plugins = require("gulp-load-plugins")({
    pattern: ['gulp-*', 'gulp.*', 'main-bower-files'],
    replaceString: /\bgulp[\-.]/
});

// define the default task and add the watch task to it
gulp.task('default', ['watch']);
gulp.task('build', ['css', 'js']);

// configure the jshint task
gulp.task('jshint', function() {
  return gulp.src('source/javascript/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});
gulp.task('js', function() {
  var jsFiles = ['source/javascript/*.js'];
  return gulp.src(plugins.mainBowerFiles().concat(jsFiles))
    .pipe(plugins.filter('*.js'))
    .pipe(plugins.concat('mickem-bootstrap.js'))
    .pipe(gutil.env.type === 'production' ? plugins.uglify() : gutil.noop()) 
    .pipe(gulp.dest('static/js'));
});
gulp.task('css', function() {
  var cssFiles = ['source/css/*'];
  gulp.src(plugins.mainBowerFiles().concat(cssFiles))
    .pipe(plugins.filter('*.css'))
    .pipe(plugins.concat('mickem-bootstrap.css'))
    .pipe(gutil.env.type === 'production' ? plugins.minifyCss() : gutil.noop()) 
    .pipe(gulp.dest('static/css'));
 });
gulp.task('watch', function() {
  gulp.watch('source/js/*', ['js']);
  gulp.watch('source/css/*', ['css']);
});