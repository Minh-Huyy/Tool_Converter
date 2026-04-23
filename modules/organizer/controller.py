from .service import FileOrganizerService

class OrganizerController:
    @classmethod
    def handle_organize(cls, folder_path: str) -> tuple[bool, str, list[str]]:
        if not folder_path:
            return False, "Vui lòng chọn thư mục.", []
        return FileOrganizerService.organize_folder(folder_path)
