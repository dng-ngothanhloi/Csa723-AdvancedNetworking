# Changelog - Script tạo GitHub Issues

## Version 2.0.0 - 2024-12-19

### ✨ Tính năng mới

#### 1. Hỗ trợ tham số file input
- Script giờ đây nhận tham số file input: `./create_issues.sh <input_file> [repository]`
- Không còn hardcode tên file `TaskList.md`

#### 2. Hệ thống template linh hoạt
- Tự động chọn template dựa trên tên file:
  - `Tasklist-*.md` → `task-request` template
  - `Featurelist-*.md` → `feature_request` template  
  - `RequirementList-*.md` → `feature_request` template
  - `FunctionList-*.md` → `feature_request` template
  - `Feedbacklist-*.md` → `bug_report` template
  - `BugList-*.md` → `bug_report` template
  - `IssueList-*.md` → `bug_report` template

#### 3. Template mới được tạo
- **task-request.md**: Template cho các task nghiên cứu/phát triển
- **feature_request.md**: Template cho các tính năng mới
- **bug_report.md**: Template cho báo cáo lỗi

#### 4. Cải tiến xử lý lỗi
- Kiểm tra file tồn tại
- Kiểm tra GitHub CLI đã cài đặt
- Kiểm tra đăng nhập GitHub
- Thông báo lỗi rõ ràng với hướng dẫn khắc phục

#### 5. Cải tiến parsing
- Xử lý chính xác hơn các section mô tả và output
- Hỗ trợ format markdown với bullet points
- Xử lý task cuối cùng trong file

### 📁 Files được tạo/cập nhật

#### Files mới:
- `Tasklist-NOMA.md` - Task list cho dự án NOMA Security
- `.github/ISSUE_TEMPLATE/feature_request.md` - Template cho feature request
- `.github/ISSUE_TEMPLATE/bug_report.md` - Template cho bug report
- `README-create-issues.md` - Hướng dẫn sử dụng chi tiết
- `test_create_issues.sh` - Script test
- `CHANGELOG-create-issues.md` - File này

#### Files được cập nhật:
- `create_issues.sh` - Script chính được cải tiến hoàn toàn
- `.github/ISSUE_TEMPLATE/task-request.md` - Template được cập nhật

### 🔧 Cải tiến kỹ thuật

#### 1. Cấu trúc code
- Tách biệt logic tạo template thành các hàm riêng
- Sử dụng case statement để chọn template
- Cải thiện khả năng đọc và bảo trì

#### 2. Validation
- Kiểm tra tham số đầu vào
- Validation file tồn tại
- Kiểm tra môi trường (GitHub CLI)

#### 3. Output
- Thông báo tiến trình rõ ràng
- Hiển thị template được sử dụng
- Link đến issues sau khi tạo

### 📋 Template Fields

Tất cả template đều có các field chung:
- **Status**: To Do (mặc định)
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025

#### Task Request:
- **Type**: Task
- **Category**: Sourcecode
- **Labels**: task

#### Feature Request:
- **Type**: Feature
- **Category**: Feature
- **Labels**: enhancement

#### Bug Report:
- **Type**: Bug
- **Category**: Bug
- **Labels**: bug

### 🚀 Cách sử dụng

#### Cú pháp cơ bản:
```bash
./create_issues.sh <input_file> [repository]
```

#### Ví dụ:
```bash
# Tạo issues từ Tasklist-NOMA.md
./create_issues.sh Tasklist-NOMA.md dng-ngothanhloi/isa701-csdl

# Test script trước khi chạy
./test_create_issues.sh
```

### 🔄 Migration từ version cũ

Nếu bạn đang sử dụng version cũ:
1. Backup script cũ
2. Thay thế bằng script mới
3. Cấp quyền thực thi: `chmod +x create_issues.sh`
4. Chạy test: `./test_create_issues.sh`
5. Sử dụng với tham số file: `./create_issues.sh Tasklist-NOMA.md`

### 📚 Documentation

- `README-create-issues.md` - Hướng dẫn chi tiết
- `test_create_issues.sh` - Script test và validation
- Template files trong `.github/ISSUE_TEMPLATE/`

### 🐛 Bug fixes

- Sửa lỗi parsing không chính xác với format markdown
- Sửa lỗi không xử lý task cuối cùng
- Cải thiện xử lý lỗi và thông báo

### 🔮 Roadmap

- [ ] Hỗ trợ custom deadline từ file input
- [ ] Hỗ trợ assignee từ file input
- [ ] Hỗ trợ multiple labels
- [ ] Dry-run mode để preview
- [ ] Batch processing nhiều file
- [ ] Export issues sang CSV/Excel 