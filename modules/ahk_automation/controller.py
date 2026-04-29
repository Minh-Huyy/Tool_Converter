from .service import AHKService

class AHKController:
    def __init__(self):
        self.service = AHKService()

    def run_automation(self, config):
        # 1. Update config
        success, msg = self.service.update_script_config(config)
        if not success:
            return False, msg
        
        # 2. Start script
        return self.service.start_script()

    def stop_automation(self):
        return self.service.stop_script()

    def get_status(self):
        return self.service.is_running()
