o
    �i�g  �                
   @   s�   d dl mZmZmZ d dlmZ ddlmZ ddlm	Z	m
Z
mZ e� Ze�d�ee�fdeded	efd
d��Ze�d�ee�fdededed	efdd��Ze�d�ee�fdefdd��Ze�d�dd� �ZdS )�    )�	APIRouter�Depends�Header)�Session�   )�get_db)�register_user�login�verify_tokenz
/register/�username�password�dbc                 C   s   t || |�S �N)r   )r   r   r   � r   �/app/routes/usuario_routes.py�register   s   r   z/login/�emailc                 C   s   t || ||�S r   )r	   )r   r   r   r   r   r   r   �
user_login   s   r   z/protected/c                 C   s   dd| � d�iS )N�messagezBem-vindo, u   ! Esta é uma rota protegida.r   )r   r   r   r   �protected_route   s   r   z/healthc                   C   s   ddiS )N�status�okr   r   r   r   r   �health_check   s   r   N)�fastapir   r   r   Zsqlalchemy.ormr   Zmodels.databaser   Zcontrollers.user_controllerr   r	   r
   �router�post�strr   r   �getr   r   r   r   r   r   �<module>   s     $