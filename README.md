# Atlassian MCP Server

A Model Context Protocol (MCP) server that provides comprehensive integration with Atlassian Jira and Confluence. This server allows LLMs to interact with your Atlassian suite to search, view, and modify issues and pages.

## Features

### Jira Tools
- **Search**: Find issues using JQL (`searchJiraIssuesUsingJql`).
- **Issue Management**: 
  - Get issue details (`getJiraIssue`).
  - Create (`createJiraIssue`) and edit (`editJiraIssue`) issues.
  - view remote links (`getJiraIssueRemoteIssueLinks`).
- **Comments & Worklogs**: Add comments (`addCommentToJiraIssue`) and worklogs (`addWorklogToJiraIssue`).
- **Metadata**: Inspect issue types (`getJiraProjectIssueTypesMetadata`, `getJiraIssueTypeMetaWithFields`).
- **Transitions**: View (`getTransitionsForJiraIssue`) and execute (`transitionJiraIssue`) workflow transitions.
- **Projects & Users**: List visible projects (`getVisibleJiraProjects`) and look up account IDs (`lookupJiraAccountId`).

### Confluence Tools
- **Search**: Find pages using CQL (`searchConfluenceUsingCql`).
- **Page Management**: 
  - Get page content (`getConfluencePage`).
  - Create (`createConfluencePage`) and update (`updateConfluencePage`) pages.
  - List descendants (`getConfluencePageDescendants`) and pages in a space (`getPagesInConfluenceSpace`).
- **Comments**: 
  - Add footer (`createConfluenceFooterComment`) and inline (`createConfluenceInlineComment`) comments.
  - Read comments (`getConfluencePageFooterComments`, `getConfluencePageInlineComments`).
- **Spaces**: List available spaces (`getConfluenceSpaces`).

## Prerequisites

- Python 3.10 or higher
- An Atlassian account (Jira/Confluence Cloud)
- An Atlassian API Token

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd Atlassian-MCP-Server
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```

2.  Add your Atlassian credentials to `.env`:
    ```env
    ATLASSIAN_EMAIL=your_email@example.com
    ATLASSIAN_API_TOKEN=your_api_token
    ATLASSIAN_BASE_URL=https://your-domain.atlassian.net
    ```

    > **Note**: You can generate an API Token from your [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens).

## Usage

### Running Locally
To run the server specifically (though typically used via an MCP client):
```bash
python server.py
```

### Using with Claude Desktop
To use this server with Claude Desktop, add the following configuration to your `claude_desktop_config.json` (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "/path/to/Atlassian-MCP-Server/.venv/bin/python",
      "args": [
        "/path/to/Atlassian-MCP-Server/server.py"
      ]
    }
  }
}
```
*Replace `/path/to/Atlassian-MCP-Server` with the absolute path to your cloned repository.*

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
