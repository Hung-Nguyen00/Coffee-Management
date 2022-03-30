from rolepermissions.roles import AbstractUserRole


class ProjectManager(AbstractUserRole):
    role = "Project Manager"
    description = "Manage Projects"
    available_permissions = {
        "manage_projects": True,
    }


class HumanResource(AbstractUserRole):
    role = "Human Resource"
    description = "Manage Employees"
    available_permissions = {
        "manage_employees": True,
    }


class Admin(AbstractUserRole):
    role = "Admin"
    description = "Manage Everything"
    available_permissions = {
        "manage_projects": True,
        "manage_employees": True,
    }


class Staff(AbstractUserRole):
    role = "Staff"
    description = "Manage self-info"
    available_permissions = {
        "manage_self_info": True,
    }
