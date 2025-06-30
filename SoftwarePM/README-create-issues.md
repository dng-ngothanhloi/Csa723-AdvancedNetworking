# Hướng dẫn sử dụng Script tạo GitHub Issues

## Tổng quan
Script `create_issues.sh` tự động tạo GitHub Issues từ các file markdown chứa danh sách task/feature/bug theo template tương ứng.

## Cài đặt yêu cầu

### 1. GitHub CLI
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install gh -y

# macOS
brew update
brew install gh

# Windows
winget install GitHub.cli
```

### 2. Đăng nhập GitHub CLI
```bash
gh auth login
# Chọn GitHub.com, HTTPS, và làm theo hướng dẫn
```

### 3. Cấp quyền thực thi cho script
```bash
chmod +x create_issues.sh
```

## Cách sử dụng

### Cú pháp cơ bản
```bash
./create_issues.sh <input_file> [repository]
```

### Ví dụ sử dụng
```bash
# Tạo issues từ Tasklist-NOMA.md
./create_issues.sh Tasklist-NOMA.md dng-ngothanhloi/Csa723-AdvancedNetworking

# Tạo issues từ file khác (sử dụng repository mặc định)
./create_issues.sh Featurelist-UI.md

# Tạo issues từ BugList.md
./create_issues.sh BugList.md my-org/my-repo
```

## Quy tắc chọn template

Script tự động chọn template dựa trên tên file:

| Pattern | Template | Labels |
|---------|----------|--------|
| `Tasklist-*.md` | `task-request` | `task` |
| `Featurelist-*.md` | `feature_request` | `enhancement` |
| `RequirementList-*.md` | `feature_request` | `enhancement` |
| `FunctionList-*.md` | `feature_request` | `enhancement` |
| `Feedbacklist-*.md` | `bug_report` | `bug` |
| `BugList-*.md` | `bug_report` | `bug` |
| `IssueList-*.md` | `bug_report` | `bug` |
| Khác | `task-request` | `task` |

## Định dạng file input

File markdown phải có định dạng như sau:

```markdown
# Tiêu đề file

## 1. Tên task/feature/bug
- **Mô tả:** Mô tả chi tiết nhiệm vụ
- **Output:**
  - Output 1
  - Output 2
  - Output 3

---

## 2. Tên task/feature/bug khác
- **Mô tả:** Mô tả chi tiết nhiệm vụ
- **Output:**
  - Output 1
  - Output 2
```

## Template fields

### Task Request Template
- **Status**: To Do
- **Type**: Task
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025
- **Category**: Sourcecode

### Feature Request Template
- **Status**: To Do
- **Type**: Feature
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025
- **Category**: Feature

### Bug Report Template
- **Status**: To Do
- **Type**: Bug
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025
- **Category**: Bug

## Xử lý lỗi

### Lỗi thường gặp

1. **GitHub CLI chưa cài đặt**
   ```
   Error: GitHub CLI (gh) is not installed!
   ```
   **Giải pháp:** Cài đặt GitHub CLI theo hướng dẫn trên

2. **Chưa đăng nhập GitHub**
   ```
   Error: Not logged in to GitHub CLI!
   ```
   **Giải pháp:** Chạy `gh auth login`

3. **File không tồn tại**
   ```
   Error: File Tasklist-NOMA.md not found!
   ```
   **Giải pháp:** Kiểm tra đường dẫn file

4. **Không có quyền tạo issues**
   ```
   HTTP 403: Resource not accessible by integration
   ```
   **Giải pháp:** Kiểm tra quyền truy cập repository

## Ví dụ thực tế

### Tạo issues từ Tasklist-NOMA.md
```bash
./create_issues.sh Tasklist-NOMA.md dng-ngothanhloi/isa701-csdl
```

Kết quả:
```
Using template: task-request for file: Tasklist-NOMA.md
Starting to create issues from Tasklist-NOMA.md...
Repository: dng-ngothanhloi/isa701-csdl
Template: task-request
---
Creating issue: Thiết lập môi trường nghiên cứu & chuẩn bị team work
Issue created successfully!
---
Creating issue: Tạo Báo cáo nghiên cứu chi tiết (Word & Slide tóm tắt)
Issue created successfully!
---
...
All issues created successfully!
Check your issues at: https://github.com/dng-ngothanhloi/isa701-csdl/issues
```

## Tùy chỉnh

### Thay đổi repository mặc định
Sửa dòng này trong script:
```bash
REPO="${2:-dng-ngothanhloi/isa701-csdl}"
```

### Thêm template mới
1. Tạo file template trong `.github/ISSUE_TEMPLATE/`
2. Thêm case trong hàm `get_template()`
3. Tạo hàm `create_new_template_issue_body()`
4. Thêm case trong hàm `create_issue_body()`

## Lưu ý

- Script sẽ tạo issues với trạng thái "To Do" mặc định
- Mỗi issue sẽ có label tương ứng với template
- Deadline mặc định là 13/07/2025
- Có thể chỉnh sửa các field trong template sau khi tạo 