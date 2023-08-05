# Hardware values for defects
class Hardware:
    ALL = "All"
    PC = "PC"
    MACINTOSH = "Macintosh"
    OTHERS = "Others"


# OS values for defects
class OS:
    WINDOWS = "Windows"
    MAC_OS = "Mac OS"
    LINUX = "Linux"
    OTHERS = "Others"
    ALL = "All"


# Severity values for defects
class Severity:
    FATAL = "Fatal"
    MAJOR = "Major"
    MINOR = "Minor"
    TRIVIAL = "Trivial"
    SUGGESTION = "Suggestion"
    BLOCKER = "Blocker"


# Priority values for defects
class Priority:
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


# Status values for defects
class Status:
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    REJECTED = "REJECTED"
    VERIFIED = "VERIFIED"
    REOPENED = "REOPENED"
    CLOSED = "CLOSED"
