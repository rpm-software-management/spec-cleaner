Name:           sourcelist-classes
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/sourcelist-classes

%description
Test package.

%generate_buildrequires
echo looking for the build requires
%configure
%{suseupdateconfig}

%changelog
