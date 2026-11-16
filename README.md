# Blender AI Assistant

**Version:** 0.3.4\
**Author:** Daniel Isangedighi\
**Blender compatibility declared by the add-on:** Blender 5.2.0 and
later 5.2.x releases

A lightweight Blender sidebar add-on that demonstrates a basic
AI-assistant interface, captures a small amount of scene context, and
stores a conversation in the current Blender scene.

> **Important --- current implementation is a UI prototype.** The
> `Endpoint` field is displayed but is not used. The Send Message
> operator does not call an AI service; it adds a simulated reply in the
> form `Received: <your prompt>`. No network request, authentication,
> model inference, or external AI integration is implemented yet.

## Features

-   Adds an **AI Assistant** tab to the 3D Viewport sidebar.
-   Displays current Blender workspace, mode, active object, and scene
    object count.
-   Captures a small scene snapshot containing the scene name, total
    object count, and selected object names.
-   Stores user messages and simulated assistant replies in scene
    properties.
-   Shows the latest six messages in the panel.
-   Provides a button to clear the conversation.

## Requirements

-   Blender **5.2.x**.
-   No additional Python packages are required.
-   The add-on uses Blender's built-in Python API (`bpy`).

## Installation

The supplied script is a **legacy single-file Blender add-on**. Blender
5.2 continues to support legacy add-ons and allows installing a `.py`
file from disk.

1.  Copy the add-on code into a plain-text editor.

2.  Save the file with a Python filename, for example:
    `blender_ai_assistant.py`

    Make sure the file extension is `.py`, not `.txt`.

3.  Open Blender 5.2.x.

4.  Open **Edit → Preferences**.

5.  Open the **Add-ons** section (in some Blender layouts this is
    accessible from the Extensions/Add-ons preferences).

6.  Open the Add-on settings menu and choose **Install from Disk**.

7.  Browse to `blender_ai_assistant.py` and select it.

8.  The add-on will be installed but may not be enabled automatically.
    Find **Blender AI Assistant** in the add-on list and enable its
    checkbox.

9.  Close Preferences.

Official Blender documentation: [Add-ons --- Blender 5.2
Manual](https://docs.blender.org/manual/en/5.2/editors/preferences/addons.html).

### Alternative: install by placing the script in an add-ons folder

You can also install it manually:

1.  Locate or create a Blender user scripts directory.
2.  Inside it, create a folder named `addons`.
3.  Put `blender_ai_assistant.py` inside that `addons` folder.
4.  In Blender, open **Edit → Preferences → File Paths** and add the
    parent user scripts directory under **Script Directories**.
5.  Save Preferences and restart Blender.
6.  Open the Add-ons preferences and enable **Blender AI Assistant**.

Blender's File Paths documentation explains the required
`scripts/addons` directory structure: [File Paths --- Blender 5.2
Manual](https://docs.blender.org/manual/en/5.2/editors/preferences/file_paths.html).

## Open the AI Assistant panel

1.  Switch to the **3D Viewport**.
2.  Move the pointer over the viewport and press **N** to open the
    Sidebar if it is hidden.
3.  Select the **AI Assistant** tab.
4.  The panel titled **Blender AI Assistant v0.4.0** should appear.

If the tab is not visible, confirm that the add-on is enabled and that
the active editor is the 3D Viewport.

## How to use it

### 1. Inspect the Blender context

The **Blender Context** section displays:

-   **Workspace:** the active workspace name.
-   **Mode:** the current Blender context mode, such as Object Mode or
    Edit Mode.
-   **Active:** the name of the active object, or `None`.
-   **Objects:** the number of objects in the current scene.

These values are read from Blender's current context when the panel is
drawn.

### 2. Capture the scene

1.  Arrange or select the objects you want to include in the snapshot.
2.  Click **Capture Scene**.
3.  The add-on stores a text representation of:
    -   the scene name;
    -   the total number of objects in the scene;
    -   the names of the currently selected objects.
4.  Blender displays an informational report: **Scene captured for
    grounding**.

The captured snapshot is stored in the scene property
`last_scene_snapshot`. In this version, the snapshot is not displayed in
the panel or automatically attached to a chat message. It is also not a
full geometry, mesh, material, modifier, or object-transform export.

### 3. Send a prompt

1.  Click the **Prompt** field.
2.  Type a message, for example:
    `Explain the objects currently in my scene.`
3.  Click **Send Message**.
4.  Your prompt is added to the conversation as a `YOU` message.
5.  A simulated assistant response is added:
    `Received: Explain the objects currently in my scene.`

The most recent six conversation entries are displayed in the
**Conversation** section. The prompt field is cleared after sending.

**Note:** The example prompt is not actually interpreted by an AI model
in this version. The add-on simply echoes the text with a `Received:`
prefix.

### 4. Enter an endpoint

The **Endpoint** field is reserved for a future AI-service integration.
You may enter a URL for planning purposes, but the current code does not
read or use this value. Entering an endpoint does not connect Blender to
a server.

### 5. Clear the conversation

Click **Clear Conversation** to remove all stored conversation messages
for the current scene. This does not delete Blender objects or clear the
captured scene snapshot.

## Where the data is stored

The add-on registers an `ai_assistant` property group on
`bpy.types.Scene`. Its settings and conversation are therefore
associated with the current Blender scene and are saved as part of the
`.blend` file when that file is saved.

The principal properties are:

  Property                Purpose
  ----------------------- --------------------------------------------------
  `endpoint`              Text field reserved for a future service URL
  `prompt`                Current prompt text
  `messages`              Collection of user and assistant message entries
  `active_message`        Index set to the latest message after sending
  `last_scene_snapshot`   String containing the captured scene summary

## Troubleshooting

### The AI Assistant tab is missing

-   Confirm the add-on is enabled in Preferences.
-   Move the mouse pointer over the 3D Viewport and press **N**.
-   Look for the **AI Assistant** tab in the Sidebar.
-   Confirm you are in the 3D Viewport, not the Image Editor, Outliner,
    or another editor.

### Blender reports an error when enabling the add-on

-   Confirm the file is saved as a `.py` file.
-   Check that the complete code was copied, including the `register()`
    and `unregister()` functions.
-   Open Blender's system console to inspect the Python traceback.
-   If you edited the script while Blender was open, disable and
    re-enable the add-on or use the add-on preferences' local refresh
    option.

### The assistant does not provide an AI-generated answer

That is expected in version 0.3.4. The current `AI_OT_Send.execute()`
method creates a local echo response and contains no HTTP request or
model call. An AI backend must be implemented before real AI responses
are possible.

## Current limitations and development notes

-   No AI provider or model is connected.
-   No HTTP request is made.
-   The endpoint field is not consumed by the code.
-   No API key, authentication, timeout, retry, or error handling is
    implemented.
-   Scene capture records only the scene name, object count, and
    selected object names.
-   The captured snapshot is stored but is not yet passed to the
    assistant.
-   Conversation messages are plain text and are not streamed.
-   Conversation content is stored per scene in the `.blend` file.

### Version label note

The metadata declares the add-on version as **0.3.4**, while the panel
title and description string say **v0.4.0**. This README uses **0.3.4**
as the code's declared add-on version. Consider aligning these labels in
a future code revision.

## Suggested next development steps

1.  Connect `AI_OT_Send.execute()` to a backend or AI API.
2.  Read and validate the configured endpoint.
3.  Send the prompt and a structured scene snapshot to the backend.
4.  Add secure credential handling; do not hard-code API keys in the
    add-on.
5.  Add request timeout, error handling, and user-visible connection
    status.
6.  Consider moving network work off Blender's UI thread so slow
    requests do not freeze the interface.
7.  Add controls for conversation history, context selection, and
    response display.

## License

No license is specified in the supplied source code. Add a license
before distributing the add-on publicly.

------------------------------------------------------------------------

**Author:** Daniel Isangedighi\
**Project:** Blender AI Assistant
