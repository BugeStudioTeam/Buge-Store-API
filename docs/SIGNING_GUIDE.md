# APK Signing Guide for Buge Store

This guide explains how to generate and verify the signature fingerprint for your APK.

## What is a Signature Fingerprint?

A signature fingerprint is a unique identifier derived from the certificate used to sign your APK. It ensures that your application comes from you and has not been tampered with.

## Generating Your Fingerprint

### Method 1: Using keytool (Recommended)

If you have your keystore file:

```
keytool -list -v -keystore your-keystore.keystore -alias your-alias -storepass your-password
```

Look for the `SHA1` fingerprint in the output:

```
Certificate fingerprints:
         SHA1: AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:12
```

### Method 2: Using jarsigner

```
jarsigner -verify -verbose -certs your-app.apk
```

### Method 3: Using apksigner

```
apksigner verify --verbose your-app.apk
```

## Verifying an APK's Fingerprint

### Using Android SDK tools

```
keytool -printcert -jarfile your-app.apk
```

### Using Python

```
import zipfile
import hashlib

def get_apk_signature(apk_path):
    # This is a simplified example
    # Production code should use proper APK signature verification
    with zipfile.ZipFile(apk_path, 'r') as apk:
        # Extract META-INF files and verify signatures
        pass
```

## Important Notes

1. Never share your keystore file or passwords
2. Keep your keystore in a secure location
3. The fingerprint must match for all versions of your app
4. If you lose your keystore, you cannot update your app

## Example

Your `stable.yml` should include:

```
signature_fingerprint: "AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:12"
```

## Troubleshooting

### Fingerprint mismatch error

- Ensure you are using the same keystore for all builds
- Check that you are not using debug keystore for release builds
- Verify the format matches exactly

### Cannot find fingerprint

- Make sure your APK is properly signed
- Try using `jarsigner -verify -verbose -certs app.apk` for detailed output