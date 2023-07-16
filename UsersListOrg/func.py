# from UsersListOrg.models import User
#
#
# def get_chapters_grades():
#     users = User.query.all()
#     chapters = []
#     grades = []
#     for member in users:
#         if len(grades) == 0:
#             grades.append(member.grade)
#         else:
#             for grade in grades:
#                 if member.grade != grade:
#                     grades.append(member.grade)
#         if len(chapters) == 0:
#             chapters.append(member.grade)
#         else:
#             for chapter in chapters:
#                 if member.chapter != chapter:
#                     chapters.append(member.chapter)
#     return chapters, grades
#
#
# def get_choises():
#     users = User.query.all()
#     chapters = []
#     grades = []
#     for member in users:
#         if len(grades) == 0:
#             grades.append(member.grade)
#         else:
#             for grade in grades:
#                 if member.grade != grade:
#                     grades.append(member.grade)
#         if len(chapters) == 0:
#             chapters.append(member.grade)
#         else:
#             for chapter in chapters:
#                 if member.chapter != chapter:
#                     chapters.append(member.chapter)
#     return [(str(index + 1), grade) for index, grade in enumerate(grades)]
