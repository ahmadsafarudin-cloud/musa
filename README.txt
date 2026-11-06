SAFAR ANTI-BOTNET SECURITY — Windows EXE Build Package

IMPORTANT PRODUCT STATUS
This is an early security-assistant prototype, NOT a certified antivirus and NOT a complete botnet-removal product. It currently:
- Starts a Microsoft Defender quick scan on Windows, when Defender's command-line tool is available.
- Displays a snapshot of active network connections using netstat.
- Performs a basic folder review based on selected file extensions.
- Does not provide kernel-level or real-time protection, cloud reputation, automatic quarantine, or guaranteed botnet detection.
Keep Microsoft Defender real-time protection and Windows Update enabled.

BUILD OPTION 1 — Build directly on Windows
1. Extract this ZIP on Windows 10/11.
2. Install Python 3.10+ and enable "Add Python to PATH".
3. Open the extracted folder.
4. Double-click BUILD_EXE.bat.
5. Find dist\SAFAR_ANTI_BOTNET.exe after a successful build.

BUILD OPTION 2 — Build using GitHub Actions (no local Windows compiler needed)
1. Sign in to GitHub and create a new EMPTY repository.
2. Upload the contents of this package to the repository's main branch. Make sure the .github/workflows/build-windows.yml file is included.
3. Open the repository's Actions tab.
4. Select "Build SAFAR Windows EXE" and click "Run workflow" (or let the first push trigger it).
5. Wait for the workflow to finish successfully.
6. Open the completed workflow run, scroll to Artifacts, and download SAFAR_ANTI_BOTNET-Windows. Extract it to get SAFAR_ANTI_BOTNET.exe.

The GitHub Actions method builds the EXE on a hosted Windows runner. This package itself does not yet contain the compiled EXE.

SAFE USE
- A suspicious extension or unfamiliar network connection is not proof of malware.
- Review findings before taking action; this prototype does not delete or block anything.
- For suspected infection, use Microsoft Defender's full/offline scan and seek qualified incident-response help for serious cases.
