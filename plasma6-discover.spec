%define stable %([ "$(echo %{version} |cut -d. -f3)" -ge 70 ] && echo -n un; echo -n stable)
%define git 20231023

Summary:	Plasma 6 package manager
Name:		plasma6-discover
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
License:	GPLv2+
Group:		Graphical desktop/KDE
Url:		https://www.kde.org/
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/discover/-/archive/master/discover-master.tar.bz2#/discover-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}.tar.xz
%endif
Source1:	discoverrc
Patch0:		discover-5.17.5-default-sort-by-name.patch
Patch1:		discover-dont-switch-branches.patch
# (tpg) always force refresh, periodic refresh set to 12h instead of 24h
Patch2:		https://src.fedoraproject.org/rpms/plasma-discover/raw/rawhide/f/discover-5.21.4-pk_refresh_force.patch
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(AppStreamQt) >= 0.10.4
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6WebView)
BuildRequires:	cmake(Qca-qt6)
#BuildRequires:	pkgconfig(QtOAuth)
BuildRequires:	cmake(packagekitqt6)
BuildRequires:	cmake(AppStreamQt) >= 1.0
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6Solid)
BuildRequires:	cmake(KF6Archive)
BuildRequires:	cmake(KF6TextWidgets)
BuildRequires:	cmake(KF6Attica)
BuildRequires:	cmake(KF6NewStuff)
BuildRequires:	cmake(KF6KirigamiAddons)
BuildRequires:	cmake(KF6Notifications)
BuildRequires:	cmake(KF6Package)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Plasma)
BuildRequires:	cmake(KF6Wallet)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6Declarative)
BuildRequires:	cmake(KF6ItemModels)
BuildRequires:	cmake(KF6Kirigami2)
BuildRequires:	cmake(KF6Service)
BuildRequires:	cmake(KF6Bookmarks)
BuildRequires:	cmake(KF6Completion)
BuildRequires:	cmake(KF6ItemViews)
BuildRequires:	cmake(KF6JobWidgets)
BuildRequires:	cmake(KF6Solid)
BuildRequires:	cmake(KF6Auth)
BuildRequires:	cmake(KF6Codecs)
BuildRequires:	cmake(KF6ConfigWidgets)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(KF6IdleTime)
BuildRequires:	cmake(KF6Purpose)
BuildRequires:	cmake(KF6StatusNotifierItem)
BuildRequires:	cmake(KUserFeedbackQt6)
BuildRequires:	git-core
BuildRequires:	pkgconfig(flatpak)
BuildRequires:	pkgconfig(libmarkdown)
# Don't pull in Plasma 5
BuildRequires:	plasma6-xdg-desktop-portal-kde
%ifarch %{x86_64} %{ix86} %{aarch64}
BuildRequires:	pkgconfig(fwupd)
Recommends:	%{name}-backend-fwupd
%endif
Requires:	%{name}-backend-kns
Recommends:	%{name}-backend-packagekit
Recommends:	%{name}-backend-flatpak

%description
Plasma 6 package manager.

%files -f all.lang
%{_datadir}/qlogging-categories6/discover.categories
%dir %{_libdir}/plasma-discover
%{_datadir}/kxmlgui5/plasmadiscover
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/discoverrc
%{_bindir}/plasma-discover
%{_bindir}/plasma-discover-update
%{_libdir}/plasma-discover/libDiscoverCommon.so
%{_libdir}/plasma-discover/libDiscoverNotifiers.so
%{_iconsdir}/hicolor/*/apps/plasmadiscover.*
%{_datadir}/knotifications6/discoverabstractnotifier.notifyrc
%{_datadir}/metainfo/org.kde.discover.appdata.xml
%{_qtdir}/plugins/plasma/kcms/systemsettings/kcm_updates.so

#----------------------------------------------------------------------------

%package backend-kns
Summary:	KNewStuff backend for %{name}
Group:		Graphical desktop/KDE
%rename muon-backend-kns

%description backend-kns
KNewStuff backend for %{name}.

%files backend-kns
%{_qtdir}/plugins/discover/kns-backend.so

#----------------------------------------------------------------------------

%package backend-packagekit
Summary:	PackageKit backend for %{name}
Group:		Graphical desktop/KDE
%rename muon-backend-packagekit
Requires:	packagekit
Requires:	dnf-plugins-core

%description backend-packagekit
PackageKit backend for %{name}.

%files backend-packagekit
%{_qtdir}/plugins/discover/packagekit-backend.so
%{_qtdir}/plugins/discover-notifier/DiscoverPackageKitNotifier.so
%{_datadir}/libdiscover/categories/packagekit-backend-categories.xml
%{_datadir}/metainfo/org.kde.discover.packagekit.appdata.xml

#----------------------------------------------------------------------------

%package backend-flatpak
Summary:	Flatpak backend for %{name}
Group:		Graphical desktop/KDE
Requires:	flatpak >= 0.8.7
Requires:	(flatpak-kcm if plasma-systemsettings)

%description backend-flatpak
Flatpak backend for %{name}.

%files backend-flatpak
%{_qtdir}/plugins/discover/flatpak-backend.so
%{_qtdir}/plugins/discover-notifier/FlatpakNotifier.so
%{_datadir}/libdiscover/categories/flatpak-backend-categories.xml
%{_iconsdir}/hicolor/scalable/apps/flatpak-discover.svg
%{_datadir}/metainfo/org.kde.discover.flatpak.appdata.xml

#----------------------------------------------------------------------------

%ifarch %{x86_64} %{ix86} %{aarch64}
%package backend-fwupd
Summary:	Fwupd backend for %{name}
Group:		Graphical desktop/KDE
Requires:	fwupd >= 1.1.2

%description backend-fwupd
Fwupd backend for %{name}.

%files backend-fwupd
%{_qtdir}/plugins/discover/fwupd-backend.so
%endif

#----------------------------------------------------------------------------
%package notifier
Summary:	%{name} notifier
Group:		Graphical desktop/KDE
Requires:	%{name} = %{EVRD}

%description notifier
%{name} notifier plasmoid.

%files notifier
%{_sysconfdir}/xdg/autostart/org.kde.discover.notifier.desktop
%{_libdir}/libexec/DiscoverNotifier

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n discover-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
install -m 644 -p -D %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/discoverrc

%find_lang libdiscover || touch libdiscover.lang
%find_lang plasma-discover || touch plasma-discover.lang
%find_lang plasma-discover-notifier || touch plasma-discover-notifier.lang
%find_lang plasma-discover-updater || touch plasma-discover-updater.lang
%find_lang plasma_applet_org.kde.discovernotifier || touch plasma_applet_org.kde.discovernotifier.lang
%find_lang kcm_updates || touch kcm_updates.lang
cat *.lang > all.lang
