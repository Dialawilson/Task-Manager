import flet as ft
# flet is a user-inter face library


# this code is a concept of inheritance used
# this class task is define as a subclass of ft.Control and it inherits its properties and methods

class Task(ft.UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        # the super here helps to access methods
        # and attributes the parent class __init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit Task",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete Task",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update Task",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])
    # we now define a function with async and call it
    # await to pause and resume our code during execution
    # (i.e the edith function pause the code and the update function resume the code)
    async def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        self.completed = self.display_task.value
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)


class TodoApp(ft.UserControl):

    async def add_clicked(self, e):
        try:
            if self.new_task.value:
                task = Task(
                    self.new_task.value, self.task_status_change, self.task_delete
                )
                self.task.append(task)
                self.new_task.value = ""
                await self.new_task.forcus_async()
                await self.update_async()
                self.save_tasks_to_file()
        except Exception as ex:
            print(f"An error occurred: {ex}")

    async def task_status_change(self, task):
        await self.update_async()
        self.save_tasks_to_file()

    async def task_delete(self, task):
        self.tasks.remove(task)
        await self.update_async()
        self.save_tasks_to_file()
    # #############  BUILD SECTION   ####################
    # this function is responsible for creating and
    # configuring the user inter face elements (controls) for the task, it returns a
    # ft.column object that contains ft.Row which represent the display view of the task and
    # another..
    # ***THIS SECTION OF THIS PLAY IS THE VIEW SECTION OF THE CODE*****
    def build(self):
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True

        )
        # if self.new_task = " ":
        #     alert insert a text
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Display Task"), ft.Tab(
                text="Not Completed Task"), ft.Tab(text="Completed Task")],
        )

        self.items_left = ft.Text("0 items left")

        # the application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Willy Willy Manager",
                             style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Clear completed", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    async def add_clicked(self, e):
        try:
            if self.new_task.value:
                string = self.new_task.value.strip()
                if not string:
                    return
                task = Task(string,
                            self.task_status_change, self.task_delete)
                self.tasks.controls.append(task)
                self.new_task.value = ""
                await self.new_task.focus_async()
                await self.update_async()
        except Exception as ex:
            print(f"An error occurred {ex}")

    async def task_status_change(self, task):
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                await self.task_delete(task)


# ******** THE FILTER SECTION *****

    async def update_async(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "Display Task"
                or (status == "Not Completed Task" and task.completed == False)
                or (status == "Completed Task" and task.completed)
            ) #this section control the task track
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active task todo"
        await super().update_async()


async def main(page: ft.Page):
    page.title = "MANAGER WILLY"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # create app control and add it to the page
    await page.add_async(TodoApp())


ft.app(main) # this code make the app to run as the main program
