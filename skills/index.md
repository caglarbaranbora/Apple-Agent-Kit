# Skills Index

Status: Draft
Version: 0.1.0

## Purpose
Maps implementation tasks to the correct Skill.

## Discovery Rules

| Task Keywords | Load Skill |
|---|---|
| login, sign in, authentication | skills/authentication/SKILL.md |
| writing, terminology, capitalization, button label wording, inclusive writing, date/number formatting in UI | skills/style-guide/SKILL.md |
| layout, color, typography, dark mode, materials, motion, app icon, interface icon, SF Symbols, branding, accessibility design, RTL, permission prompt design, images, inclusive design | skills/human-interface-guidelines/SKILL.md |
| lists and tables, buttons, sheets, alerts, action sheet, navigation bar, tab bar, pickers, toggles, text fields, menus, touchscreen gestures, HIG components | skills/human-interface-guidelines-components/SKILL.md |
| onboarding, first-run experience, searching, search UI, settings screen, notification design, feedback, error feedback, undo, redo, HIG patterns | skills/human-interface-guidelines-patterns/SKILL.md |
| App Store submission, App Review rejection, in-app purchase, IAP, restore purchases, demo account, screenshot requirements, app description accuracy, privacy manifest, PrivacyInfo.xcprivacy, privacy nutrition label, spam app, duplicate app, minimum functionality, permission usage string | skills/app-store-review-guidelines/SKILL.md |
| SwiftUI, NavigationStack, NavigationSplitView, @State, @Binding, @Observable, ObservableObject, @Environment, GeometryReader, LazyVGrid, LazyVStack, ForEach identity, view composition, ViewBuilder, modifier order, safeAreaInset, ignoresSafeArea | skills/swiftui/SKILL.md |
| withAnimation, .animation, AnyTransition, matchedGeometryEffect, Animatable, animatableData, PhaseAnimator, KeyframeAnimator, TapGesture, LongPressGesture, DragGesture, MagnifyGesture, RotateGesture, MagnificationGesture, RotationGesture, GestureState, simultaneously, sequenced, exclusively, highPriorityGesture, simultaneousGesture | skills/swiftui-interaction/SKILL.md |
| VoiceOver, accessibilityLabel, accessibilityTraits, accessibilityValue, accessibilityHint, accessibilityAction, UIAccessibilityCustomAction, accessibilityElement, isAccessibilityElement, accessibilitySortPriority, Dynamic Type, ScaledMetric, UIFontMetrics, Reduce Motion, Reduce Transparency, Increase Contrast, Full Keyboard Access, AccessibilityFocusState, accessibilityHidden, performAccessibilityAudit, Accessibility Inspector | skills/accessibility/SKILL.md |
| UIKit, UIViewController, viewDidLoad, viewWillAppear, addChild, NSLayoutConstraint, layout anchors, UIStackView, safeAreaLayoutGuide, UINavigationController, UITabBarController, UITableViewDiffableDataSource, UICollectionViewCompositionalLayout, UICollectionViewDiffableDataSource, CellRegistration, prepareForReuse, present, dismiss, UIModalPresentationStyle | skills/uikit/SKILL.md |
| SF Symbols, Image(systemName:), UIImage(systemName:), symbolRenderingMode, SymbolVariants, variableValue, imageScale, SymbolConfiguration, preferredSymbolConfiguration, hierarchical rendering, palette rendering, multicolor rendering, symbol variant | skills/sf-symbols/SKILL.md |
| URLSession, URLRequest, URLComponents, async await network call, data(for:), JSONDecoder, Codable decoding, DecodingError, HTTPURLResponse, URLError, Task cancellation, URLSessionConfiguration, App Transport Security, ATS, NSAppTransportSecurity, Authorization header, Bearer token, 401 refresh | skills/networking/SKILL.md |
| build configuration, Debug configuration, Release configuration, .xcconfig, Build Settings, Xcode scheme, Xcode target, Signing & Capabilities, automatic signing, manual signing, provisioning profile, signing certificate, entitlements, Xcode capability, Product > Archive, Organizer, ExportOptions, distribution method, Ad Hoc, Enterprise, App Store Connect distribution, IPA export | skills/xcode/SKILL.md |
| Face ID, Touch ID, LAContext, LABiometryType, canEvaluatePolicy, evaluatePolicy, deviceOwnerAuthentication, deviceOwnerAuthenticationWithBiometrics, LAPolicy, LAError, biometryNotEnrolled, biometryLockout, NSFaceIDUsageDescription, localizedReason, localizedFallbackTitle, SecAccessControl, biometryCurrentSet, biometryAny, biometric Keychain, Enter Passcode fallback, biometric authentication | skills/local-authentication/SKILL.md |
| ATTrackingManager, requestTrackingAuthorization, trackingAuthorizationStatus, ATTrackingManagerAuthorizationStatus, ASIdentifierManager, advertisingIdentifier, IDFA, NSUserTrackingUsageDescription, App Tracking Transparency, tracking authorization | skills/app-tracking-transparency/SKILL.md |
| UNUserNotificationCenter, requestAuthorization, UNAuthorizationOptions, getNotificationSettings, UNMutableNotificationContent, UNNotificationRequest, UNTimeIntervalNotificationTrigger, UNCalendarNotificationTrigger, registerForRemoteNotifications, didRegisterForRemoteNotificationsWithDeviceToken, UNUserNotificationCenterDelegate, willPresent, didReceive, UNNotificationAction, UNTextInputNotificationAction, UNNotificationCategory, setNotificationCategories, removePendingNotificationRequests, removeDeliveredNotifications, badge count, setBadgeCount | skills/usernotifications/SKILL.md |
| PrivacyInfo.xcprivacy, privacy manifest, NSPrivacyTracking, NSPrivacyTrackingDomains, NSPrivacyCollectedDataTypes, NSPrivacyAccessedAPITypes, NSPrivacyAccessedAPITypeReasons, required reason API, App Privacy Configuration, third-party SDK signature | skills/privacy/SKILL.md |
| DateFormatter, ISO8601DateFormatter, Date.FormatStyle, RelativeDateTimeFormatter, Measurement, MeasurementFormatter, unitStyle, unitOptions, JSONEncoder, encode(to:), init(from:), CodingKeys, FileManager, Documents directory, Caches directory, Application Support directory, isExcludedFromBackup | skills/foundation/SKILL.md |
| SecItemAdd, SecItemCopyMatching, SecItemUpdate, SecItemDelete, kSecClassGenericPassword, kSecClassInternetPassword, OSStatus, errSecSuccess, errSecItemNotFound, errSecDuplicateItem, kSecAttrAccessible, kSecAttrAccessGroup, Keychain Sharing, Keychain access group, kSecValueData, Keychain, credential storage | skills/security/SKILL.md |
| StoreKit, Product.products, product.purchase, PurchaseResult, VerificationResult, currentEntitlements, transaction.finish, Transaction.updates, AppStore.sync, restore purchases, SubscriptionInfo.Status, RenewalInfo, renewalState, subscription group, in-app purchase, IAP | skills/storekit/SKILL.md |
| Sign in with Apple, AuthenticationServices, ASAuthorizationAppleIDProvider, ASAuthorizationAppleIDRequest, ASAuthorizationController, ASAuthorizationAppleIDCredential, identityToken, authorizationCode, nonce, getCredentialState, CredentialState, credentialRevokedNotification | skills/authenticationservices/SKILL.md |
| WidgetKit, Widget, WidgetBundle, WidgetConfiguration, StaticConfiguration, AppIntentConfiguration, supportedFamilies, widgetFamily, containerBackground, TimelineProvider, TimelineEntry, Timeline, TimelineReloadPolicy, placeholder, getSnapshot, getTimeline, widgetURL, Link, Button(intent:), WidgetCenter, reloadTimelines, reloadAllTimelines | skills/widgetkit/SKILL.md |
| AppIntent, @Parameter, IntentParameter, AppEnum, ParameterSummary, AppEntity, EntityQuery, EntityStringQuery, DisplayRepresentation, AppShortcutsProvider, AppShortcut, applicationName, IntentResult, ReturnsValue, ProvidesDialog, OpensIntent, perform() | skills/app-intents/SKILL.md |

## Resolution Rules

1. Match the most specific task.
2. Load exactly one primary Skill.
3. The Skill routes Knowledge Contracts.
4. If no Skill matches, stop and report a missing Skill.
