/*
	gulpfile.js
	===========
*/

var gulp         = require('gulp');
var bundleLogger = require('./gulp/util/bundleLogger');
var handleErrors = require('./gulp/util/handleErrors');

var baseDir = './dev42/frontend';



/*
 * Main Tasks
 */

gulp.task('build', ['browserify', 'jade', 'copy', 'styles', 'images']);
gulp.task('default', ['build', 'watch']);



/*
 * Watch - Watch files, trigger tasks when they are modified
 */

gulp.task('watch', function() {
	gulp.watch('src/scss/**', ['styles']);
	gulp.watch('src/images/**', ['images']);
	gulp.watch('src/templates/**', ['jade']);
	gulp.watch('src/js/**', ['browserify']);
});



/*
* Browserify - compile and move javascript
*/

//var browserify   = require('browserify');
//var watchify     = require('watchify');
//var source       = require('vinyl-source-stream');
//
//gulp.task('browserify', function() {
//
//	var bundler = watchify({
//		// Specify the entry point of your app
//		entries: ['./src/javascript/app.js']
//	});
//
//	var bundle = function() {
//		bundleLogger.start();
//
//		return bundler
//			.bundle({debug: true})
//			.on('error', handleErrors)
//			.pipe(source('app.js'))
//			.pipe(gulp.dest(baseDir + '/static/js'))
//			.on('end', bundleLogger.end);
//	};
//
//	bundler.on('update', bundle);
//
//	return bundle();
//});


var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var uglify = require('gulp-uglify');
var size = require('gulp-size');

var bundler = browserify('./src/javascript/app.js');

gulp.task('browserify', function(){
  return bundler.bundle({standalone: 'noscope'})
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(size())
    .pipe(gulp.dest(baseDir + '/static/js'));
});


/*
 * Jade - Move Jade files
 */

var jade = require('gulp-jade');

gulp.task('jade', function() {
	// @todo: Change structure so we have /templates/global, /templates/articles, /templates/events etc
	return gulp.src('./src/templates/**/*.*')
		.pipe(gulp.dest(baseDir + '/templates/'));
});



/*
 * Images - Compress and move images
 */

var changed  = require('gulp-changed');
var imagemin = require('gulp-imagemin');

gulp.task('images', function() {

	return gulp.src('./src/images/**')
		.pipe(changed(baseDir + '/static/images')) // Ignore unchanged files
//		.pipe(imagemin()) // Optimize
		.pipe(gulp.dest(baseDir + '/static/images'));
});



/*
 * SASS - Compile and move sass
 */

var sass = require('gulp-sass');

gulp.task('styles', function() {

	return gulp.src('./src/scss/app.scss')
		.pipe(sass({
			outputStyle: 'expanded',
			errLogToConsole: true
		})).on('error', handleErrors)
		.pipe(gulp.dest(baseDir + '/static/css'));
});



/*
 * Fonts - Move font files
 */

gulp.task('copy', function(){

	return gulp.src('./src/fonts/*')
		.pipe(gulp.dest(baseDir + '/static/fonts'));
});



// Helper Tasks
gulp.task('setWatch', function() {
	global.isWatching = true;
});




