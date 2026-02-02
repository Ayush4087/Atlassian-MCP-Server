from mcp.server.fastmcp import FastMCP
from tools.jira import (
    searchJiraIssuesUsingJql,
    getJiraIssue,
    addCommentToJiraIssue,
    addWorklogToJiraIssue,
    createJiraIssue,
    editJiraIssue,
    getJiraIssueRemoteIssueLinks,
    getJiraIssueTypeMetaWithFields,
    getJiraProjectIssueTypesMetadata,
    getTransitionsForJiraIssue,
    getVisibleJiraProjects,
    lookupJiraAccountId,
    transitionJiraIssue
)
from tools.confluence import (
    searchConfluenceUsingCql,
    getConfluencePage,
    createConfluenceFooterComment,
    createConfluenceInlineComment,
    createConfluencePage,
    getConfluencePageDescendants,
    getConfluencePageFooterComments,
    getConfluencePageInlineComments,
    getConfluenceSpaces,
    getPagesInConfluenceSpace,
    updateConfluencePage
)


mcp = FastMCP("jira-confluence-mcp", host="127.0.0.1", port=3334)

# ---------------- JIRA TOOLS ---------------- #

mcp.tool()(searchJiraIssuesUsingJql)
mcp.tool()(getJiraIssue)
mcp.tool()(addCommentToJiraIssue)
mcp.tool()(addWorklogToJiraIssue)
mcp.tool()(createJiraIssue)
mcp.tool()(editJiraIssue)
mcp.tool()(getJiraIssueRemoteIssueLinks)
mcp.tool()(getJiraIssueTypeMetaWithFields)
mcp.tool()(getJiraProjectIssueTypesMetadata)
mcp.tool()(getTransitionsForJiraIssue)
mcp.tool()(getVisibleJiraProjects)
mcp.tool()(lookupJiraAccountId)
mcp.tool()(transitionJiraIssue)

# ---------------- CONFLUENCE TOOLS ---------------- #

mcp.tool()(searchConfluenceUsingCql)
mcp.tool()(getConfluencePage)
mcp.tool()(createConfluenceFooterComment)
mcp.tool()(createConfluenceInlineComment)
mcp.tool()(createConfluencePage)
mcp.tool()(getConfluencePageDescendants)
mcp.tool()(getConfluencePageFooterComments)
mcp.tool()(getConfluencePageInlineComments)
mcp.tool()(getConfluenceSpaces)
mcp.tool()(getPagesInConfluenceSpace)
mcp.tool()(updateConfluencePage)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
