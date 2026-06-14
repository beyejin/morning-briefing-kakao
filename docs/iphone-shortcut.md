# iPhone Shortcut Setup

This shortcut sends the iPhone's current location to the `Morning Briefing` GitHub Actions workflow. The workflow then uses that location for weather and air quality.

## 1. Create a GitHub Token

Create a fine-grained personal access token for only this repository.

- Repository: `beyejin/morning-briefing-kakao`
- Permissions:
  - Actions: Read and write
  - Contents: Read-only

Copy the token. It is used only inside your iPhone Shortcut.

## 2. Create the Shortcut

Open the Shortcuts app on iPhone and create a new shortcut named `Send Morning Briefing`.

Add these actions in order:

1. `Get Current Location`
2. `Get Details of Location`
   - Detail: `Latitude`
   - Input: Current Location
3. `Set Variable`
   - Name: `Latitude`
4. `Get Details of Location`
   - Detail: `Longitude`
   - Input: Current Location
5. `Set Variable`
   - Name: `Longitude`
6. `Get Contents of URL`
   - URL: `https://api.github.com/repos/beyejin/morning-briefing-kakao/actions/workflows/morning-briefing.yml/dispatches`
   - Method: `POST`
   - Headers:
     - `Accept`: `application/vnd.github+json`
     - `Authorization`: `Bearer YOUR_GITHUB_TOKEN`
     - `X-GitHub-Api-Version`: `2026-03-10`
   - Request Body: JSON
     - `ref`: `main`
     - `inputs`: Dictionary
       - `latitude`: `Latitude`
       - `longitude`: `Longitude`

## 3. Automate It

In the Shortcuts app:

1. Go to `Automation`.
2. Create a new personal automation.
3. Choose `Time of Day`.
4. Set the morning time you want.
5. Choose `Run Immediately` if available.
6. Add action `Run Shortcut`.
7. Select `Send Morning Briefing`.

## Notes

The GitHub token is stored on your iPhone inside the shortcut. Keep the token scoped to this repository only.

If the shortcut does not send a location, the workflow falls back to the `LATITUDE` and `LONGITUDE` GitHub Secrets.
