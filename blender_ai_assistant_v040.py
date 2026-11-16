bl_info = {
    "name": "Blender AI Assistant",
    "author": "Daniel Isangedighi",
    "version": (0, 3, 4),
    "blender": (5, 2, 0),
    "location": "View3D > Sidebar > AI Assistant",
    "description": "Blender AI Assistant v0.4.0 - draw() safe",
    "category": "3D View",
}

import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import StringProperty, CollectionProperty, PointerProperty, IntProperty

class AIMessage(PropertyGroup):
    role: StringProperty(default='ASSISTANT')
    content: StringProperty(default='')

class AISettings(PropertyGroup):
    endpoint: StringProperty(name='Endpoint')
    prompt: StringProperty(name='Prompt')
    messages: CollectionProperty(type=AIMessage)
    active_message: IntProperty(default=0)
    last_scene_snapshot: StringProperty(default='')

class AI_OT_CaptureScene(Operator):
    bl_idname = 'ai_assistant.capture'
    bl_label = 'Capture Scene'

    def execute(self, context):
        s = context.scene.ai_assistant
        s.last_scene_snapshot = str({
            'scene': context.scene.name,
            'objects': len(context.scene.objects),
            'selected': [o.name for o in context.selected_objects]
        })
        self.report({'INFO'}, 'Scene captured for grounding')
        return {'FINISHED'}

class AI_OT_Send(Operator):
    bl_idname = 'ai_assistant.send'
    bl_label = 'Send Message'

    def execute(self, context):
        s = context.scene.ai_assistant

        if not s.prompt.strip():
            return {'CANCELLED'}

        user_msg = s.messages.add()
        user_msg.role = 'YOU'
        user_msg.content = s.prompt

        reply = s.messages.add()
        reply.role = 'ASSISTANT'
        reply.content = f'Received: {s.prompt}'

        s.prompt = ''
        s.active_message = len(s.messages) - 1
        return {'FINISHED'}

class AI_OT_Clear(Operator):
    bl_idname = 'ai_assistant.clear'
    bl_label = 'Clear Conversation'

    def execute(self, context):
        context.scene.ai_assistant.messages.clear()
        return {'FINISHED'}

class AI_PT_Main(Panel):
    bl_label = 'Blender AI Assistant v0.4.0'
    bl_idname = 'AI_PT_MAIN_V034'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI Assistant'

    def draw(self, context):
        layout = self.layout
        s = context.scene.ai_assistant

        workspace_name = context.workspace.name if context.workspace else 'Unknown'
        current_mode = context.mode
        active_name = context.active_object.name if context.active_object else 'None'
        object_count = len(context.scene.objects)

        layout.prop(s, 'endpoint', text='Endpoint')
        layout.operator('ai_assistant.capture', text='Capture Scene')

        context_box = layout.box()
        context_box.label(text='Blender Context')
        context_box.label(text=f'Workspace: {workspace_name}')
        context_box.label(text=f'Mode: {current_mode}')
        context_box.label(text=f'Active: {active_name}')
        context_box.label(text=f'Objects: {object_count}')

        if len(s.messages) > 0:
            convo = layout.box()
            convo.label(text='Conversation')
            for msg in list(s.messages)[-6:]:
                convo.label(text=f'{msg.role}: {msg.content[:90]}')

        layout.separator()
        layout.prop(s, 'prompt', text='Prompt')

        col = layout.column(align=True)
        col.scale_y = 1.2
        col.operator('ai_assistant.send', text='Send Message', icon='PLAY')
        col.operator('ai_assistant.clear', text='Clear Conversation', icon='TRASH')

classes = (
    AIMessage,
    AISettings,
    AI_OT_CaptureScene,
    AI_OT_Send,
    AI_OT_Clear,
    AI_PT_Main,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.ai_assistant = PointerProperty(type=AISettings)


def unregister():
    del bpy.types.Scene.ai_assistant
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    register()
