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
    $('#xhr-pr-rs-' + repo_name).html("<h2>Repo: " + repo_name + "</h2>");
    $.ajax({
        type: "GET",
        url: "/api/get-branches",
        data: {repo: repo_name},
        dataType: "json",
        success: function(data)
        {
            $.each(data, function(index, item) {
                var originalText = item['name'];
                var cleanedText = originalText.replace(/\./g, '') + '-' + repo_name;
                $('#xhr-pr-rs-' + repo_name).append('<div id=\"rs-' + cleanedText + '\"><h3>Branch: ' + item['name'] + '</h3></div>');
                load_pr_search_for_branch(repo_name, pr_arg, item['commit']['sha'], 'rs-' + cleanedText)
            });
        }
    });
}

function load_pr_search_for_branch(repo_arg, pr_arg, branch_sha_arg, div_id_arg)
{
    // console.log(branch_sha)
    $.ajax({
        type: "GET",
        url: "/api/find-pr-in-branch",
        data: {pr: pr_arg, branch: branch_sha_arg, repo: repo_arg},
        dataType: "json",
        success: function(data)
        {
            $.each(data, function(index, item) {
                // console.log(item);
                $('#' + div_id_arg).append(
                    "<div>" 
                        + '<a href="'
                            + "https://github.com/Graylog2/"
                            + item.repo
                            + "/blob/" 
                            + branch_sha_arg + "/"
                            + item.file
                        + '" target="_blank">'
                            + item.repo
                            + "/"
                            + item.file 
                        + "</a>"
                    + "</div>"
                );
            });
            // https://github.com/Graylog2/graylog2-server/blob/6.2/changelog/6.2.1/pr-22343.toml
            // $('#' + div_id_arg).append("" + data);
        }
    });
}