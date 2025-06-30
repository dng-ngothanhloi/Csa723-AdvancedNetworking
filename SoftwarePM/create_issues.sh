#!/bin/bash

# Script: create_issues.sh
# Tự động tạo GitHub Issues từ file markdown sử dụng GitHub CLI (gh)
# Usage: ./create_issues.sh <input_file> [repository]
# Example: ./create_issues.sh Tasklist-NOMA.md dng-ngothanhloi/isa701-csdl

# Kiểm tra tham số đầu vào
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input_file> [repository]"
    echo "Example: $0 Tasklist-NOMA.md dng-ngothanhloi/isa701-csdl"
    exit 1
fi

INPUT_FILE="$1"
REPO="${2:-dng-ngothanhloi/isa701-csdl}"

# Kiểm tra file tồn tại
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File $INPUT_FILE not found!"
    exit 1
fi

# Xác định template dựa trên tên file
get_template() {
    local filename=$(basename "$1")
    case "$filename" in
        Tasklist-*.md)
            echo "task-request"
            ;;
        Featurelist-*.md|RequirementList-*.md|FunctionList-*.md)
            echo "feature_request"
            ;;
        Feedbacklist-*.md|BugList-*.md|IssueList-*.md)
            echo "bug_report"
            ;;
        *)
            echo "task-request"  # Default template
            ;;
    esac
}

TEMPLATE=$(get_template "$INPUT_FILE")
echo "Using template: $TEMPLATE for file: $INPUT_FILE"

# Tạo issue body với template task-request
create_task_issue_body() {
    local title="$1"
    local description="$2"
    local output="$3"
    
    cat << EOF
---
name: Task request
about: Describe this issue
title: '$title'
labels: 'task'
assignees: ''

---

## Custom fields
- **Status**: To Do
- **Type**: Task
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025
- **Category**: Sourcecode

## Mô tả nhiệm vụ
$description

## Output mong muốn
$output

## Hướng dẫn thực hiện (nếu có)
<!-- Thêm hướng dẫn cụ thể hoặc tài nguyên tham khảo nếu cần thiết cho task này. -->

EOF
}

# Tạo issue body với template feature_request
create_feature_issue_body() {
    local title="$1"
    local description="$2"
    local output="$3"
    
    cat << EOF
---
name: Feature request
about: Suggest an idea for this project
title: '$title'
labels: 'enhancement'
assignees: ''

---

## Custom fields
- **Status**: To Do
- **Type**: Feature
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025
- **Category**: Feature

## Mô tả tính năng
$description

## Output mong muốn
$output

## Hướng dẫn thực hiện (nếu có)
<!-- Thêm hướng dẫn cụ thể hoặc tài nguyên tham khảo nếu cần thiết cho feature này. -->

## Acceptance Criteria
<!-- Các tiêu chí chấp nhận để feature được coi là hoàn thành -->
- [ ] 
- [ ] 
- [ ] 

## Additional context
<!-- Add any other context or screenshots about the feature request here. -->

EOF
}

# Tạo issue body với template bug_report
create_bug_issue_body() {
    local title="$1"
    local description="$2"
    local output="$3"
    
    cat << EOF
---
name: Bug report
about: Create a report to help us improve
title: '$title'
labels: 'bug'
assignees: ''

---

## Custom fields
- **Status**: To Do
- **Type**: Bug
- **Course**: CS-A723-AdvancedNetworking
- **Sprint**: AdvancedNetworking#1
- **Deadline**: 13/07/2025
- **Category**: Bug

## Mô tả lỗi
$description

## Output mong muốn
$output

## Hướng dẫn thực hiện (nếu có)
<!-- Thêm hướng dẫn cụ thể hoặc tài nguyên tham khảo nếu cần thiết cho việc sửa lỗi này. -->

## Steps to reproduce
<!-- Các bước để tái hiện lỗi -->
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected behavior
<!-- Mô tả hành vi mong đợi -->

## Actual behavior
<!-- Mô tả hành vi thực tế -->

## Screenshots
<!-- Nếu có thể, thêm screenshot để minh họa lỗi -->

## Environment
- OS: [e.g. Windows 10, macOS, Ubuntu]
- Browser: [e.g. Chrome, Firefox, Safari]
- Version: [e.g. 22]

## Additional context
<!-- Add any other context about the problem here. -->

EOF
}

# Chọn template phù hợp
create_issue_body() {
    local title="$1"
    local description="$2"
    local output="$3"
    
    case "$TEMPLATE" in
        "task-request")
            create_task_issue_body "$title" "$description" "$output"
            ;;
        "feature_request")
            create_feature_issue_body "$title" "$description" "$output"
            ;;
        "bug_report")
            create_bug_issue_body "$title" "$description" "$output"
            ;;
        *)
            create_task_issue_body "$title" "$description" "$output"
            ;;
    esac
}

# Xử lý file và tạo issues
process_file() {
    local current_title=""
    local current_description=""
    local current_output=""
    local in_output_section=false
    
    while IFS= read -r line; do
        # Tìm task mới
        if [[ $line =~ ^##[[:space:]]+[0-9]+\.[[:space:]]+(.+)$ ]]; then
            # Lưu task trước đó nếu có
            if [ -n "$current_title" ]; then
                create_issue_body "$current_title" "$current_description" "$current_output" > "issue.tmp"
                echo "Creating issue: $current_title"
                gh issue create --repo "$REPO" --title "$current_title" --body-file "issue.tmp"
                echo "Issue created successfully!"
                echo "---"
            fi
            
            # Bắt đầu task mới
            current_title="${BASH_REMATCH[1]}"
            current_description=""
            current_output=""
            in_output_section=false
            
        # Tìm mô tả
        elif [[ $line =~ ^-[[:space:]]+\*\*Mô[[:space:]]tả:\*\*(.+)$ ]]; then
            current_description="${BASH_REMATCH[1]}"
            
        # Tìm output
        elif [[ $line =~ ^-[[:space:]]+\*\*Output:\*\*$ ]]; then
            in_output_section=true
            current_output=""
            
        # Thu thập output items
        elif [ "$in_output_section" = true ] && [[ $line =~ ^[[:space:]]+-[[:space:]](.+)$ ]]; then
            if [ -n "$current_output" ]; then
                current_output="$current_output\n"
            fi
            current_output="$current_output- ${BASH_REMATCH[1]}"
        fi
    done < "$INPUT_FILE"
    
    # Xử lý task cuối cùng
    if [ -n "$current_title" ]; then
        create_issue_body "$current_title" "$current_description" "$current_output" > "issue.tmp"
        echo "Creating issue: $current_title"
        gh issue create --repo "$REPO" --title "$current_title" --body-file "issue.tmp"
        echo "Issue created successfully!"
        echo "---"
    fi
}

# Kiểm tra GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed!"
    echo "Please install it first: https://cli.github.com/"
    exit 1
fi

# Kiểm tra đăng nhập GitHub
if ! gh auth status &> /dev/null; then
    echo "Error: Not logged in to GitHub CLI!"
    echo "Please run: gh auth login"
    exit 1
fi

echo "Starting to create issues from $INPUT_FILE..."
echo "Repository: $REPO"
echo "Template: $TEMPLATE"
echo "---"

# Xử lý file
process_file

# Dọn dẹp
rm -f issue.tmp

echo "All issues created successfully!"
echo "Check your issues at: https://github.com/$REPO/issues"
