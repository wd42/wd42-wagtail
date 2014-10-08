# Compiling front end files
# -------------------------

include ../../../common.mk

# Making the assets means making all the CSS and JS files
.PHONY: assets
assets: css js

# CSS files
# ---------
.PHONY: css

# There is one global site-wide CSS file for base site styles
SITE_STYLE = css/app.css
SITE_STYLE_MIN = $(SITE_STYLE:.css=.min.css)
css: $(SITE_STYLE_MIN)

# It consists of these files, compiled, and concatenated together
SITE_CSS_SRC = \
	# End of css
SITE_SCSS_SRC = \
	css/style.scss \
	# End of scss
SITE_SCSS_OBJ = $(SITE_SCSS_SRC:.scss=.css)

# To make it, concatenate all the base styles in to one file
$(SITE_STYLE): $(SITE_CSS_SRC) $(SITE_SCSS_OBJ)
	cat $^ > $@


# JS files
# --------
.PHONY: js

# There is one global site-wide JS file for the base site scripts
SITE_SCRIPT = js/app.js
SITE_SCRIPT_MIN = $(SITE_SCRIPT:.js=.min.js)
js: $(SITE_SCRIPT_MIN)

# It consists of these files, concatenated together
SITE_SCRIPT_SRC = \
	js/script.js \
	# End of site scripts

# To make it, concatenate all the base scripts together in to one file
$(SITE_SCRIPT): $(SITE_SCRIPT_SRC)
	cat $^ > $@



# Patterns and rules
# ------------------

# How to compile SASS files to CSS files
%.css: %.scss
	$(SASSC) -C $< > $@

# Minify CSS files
%.min.css: %.css
	$(MIN_CSS) -o $@ $<

# Minify JS files
%.min.js: %.js
	$(MIN_JS) -o $@ $<


# Utilities and other bits
# ------------------------
.PHONY: clean
clean:
	rm -rf $(SITE_SCSS_OBJ)
	rm -rf $(SITE_STYLE) $(SITE_STYLE_MIN)
	rm -rf $(SITE_SCRIPT) $(SITE_SCRIPT_MIN)

watch:
	@echo Watching for changes...
	@while inotifywait -qqr --exclude '.*/\..*\.sw?' . ; do \
		sleep 0.1 ; \
		$(MAKE) --no-print-directory ; \
	done