function find_pr(pr_arg)
{
    // $.ajax({
    //     type: "GET",
    //     url: "/api/find-pr-in-branch",
    //     data: {pr: pr_arg},
    //     dataType: "json",
    //     success: function(data)
    //     {
            
    //     }
    // });

    $( document ).ready(function() {
        populate_by_repo("open", pr_arg);
        populate_by_repo("enterprise", pr_arg);
    });
}

function populate_by_repo(repo_name, pr_arg)
{
    // $("#xhr-pr-rs-" + repo_name).html("Repo: " + repo_name);
    console.log('#xhr-pr-rs-' + repo_name);
    $('#xhr-pr-rs-' + repo_name).html("<h2>Repo: " + repo_name + "</h2><div class=\"loading-gif-" + repo_name + "\"><img src=\"/files/images/loading.gif\"></div>");
    $.ajax({
        type: "GET",
        url: "/api/get-branches",
        data: {repo: repo_name},
        dataType: "json",
        success: function(data)
        {
            if ('error' in data) {
                console.log(data.error)
                $('#xhr-pr-rs-' + repo_name).append("ERROR");

                $.each(data.error, function(index, item) {
                    $('#xhr-pr-rs-' + repo_name).append(index + ": " + item);
                });
            } else {
                $('div.loading-gif-' + repo_name).html("");
                $.each(data, function(index, item) {
                    var originalText = item['name'];
                    var cleanedText = originalText.replace(/\./g, '') + '-' + repo_name;
                    $('#xhr-pr-rs-' + repo_name).append('<div id=\"rs-' + cleanedText + '\"><h3>Branch: ' + item['name'] + '</h3>');
                    if (item['name'].toLowerCase() == "master") {
                        $('#rs-' + cleanedText).append('<div class="note">NOTE: Unreleased issues/PRs will typically be released in the next minor/major version.</div>');
                    }
                    $('#xhr-pr-rs-' + repo_name).append('</div>');
                    load_pr_search_for_branch(repo_name, pr_arg, item['commit']['sha'], 'rs-' + cleanedText)
                });
            }
        },
    });
}

function load_gh_file(file_arg, div_id_arg)
{
    // http://localhost:89/api/get-file?file=
    $.ajax({
        type: "GET",
        url: "/api/get-file",
        data: {file: file_arg},
        dataType: "json",
        success: function(data)
        {
            if ('rich_content' in data) {
                // console.log("Append: " + div_id_arg);
                // console.log("With: " + data);
                $('#' + div_id_arg).append("<div class='file-contents'>" + data.rich_content.replace("\n", "<br>") + "</div>");
            }
        }
    });
}

function load_pr_search_for_branch(repo_arg, pr_arg, branch_sha_arg, div_id_arg)
{
    // console.log(branch_sha)
    $('#' + div_id_arg).append("<div class=\"loading-gif-" + div_id_arg + "\"><img src=\"/files/images/loading.gif\"></div>");
    $.ajax({
        type: "GET",
        url: "/api/find-pr-in-branch",
        data: {pr: pr_arg, branch: branch_sha_arg, repo: repo_arg},
        dataType: "json",
        success: function(data)
        {
            $('div.loading-gif-' + div_id_arg).html("");
            $.each(data, function(index, item) {
                // console.log(item);
                s_full_gh_file_url = "https://github.com/Graylog2/"
                    + item.repo
                    + "/blob/" 
                    + branch_sha_arg + "/"
                    + item.file
                
                // GET /repos/{owner}/{repo}/contents/{path}?ref={commit_sha}
                s_get_fule = ""
                    + item.repo
                    + "/contents/"
                    + item.file
                    + "?ref="
                    + branch_sha_arg
                // console.log(s_get_fule);
                // http://localhost:89/api/get-file?file=

                var originalText = item.file;
                var cleanedText = originalText.replace(/[\/\.]/g, '')
                $('#' + div_id_arg).append(
                    "<div " 
                    + 'id="'
                    + cleanedText
                    + '"'
                    + ">" 
                        + '<a href="'
                            + s_full_gh_file_url
                        + '" target="_blank">'
                            + item.repo
                            + "/"
                            + item.file 
                        + "</a>"
                    + "</div>"
                );
                load_gh_file(s_get_fule, cleanedText);
            });
            // https://github.com/Graylog2/graylog2-server/blob/6.2/changelog/6.2.1/pr-22343.toml
            // $('#' + div_id_arg).append("" + data);
        }
    });
}